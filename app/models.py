from sqlalchemy import (
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    create_engine,
    func,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from app import logger as log

Base = declarative_base()

logger = log.get_logger()


class User(Base):  # type: ignore[misc, valid-type]
    """User model.

    Represents a user in the system."""

    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    receipts = relationship("Receipt", back_populates="user")


class Product(Base):  # type: ignore[misc, valid-type]
    """Product model.

    Represents a product in the store."""

    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    price = Column(Float)
    sale_items = relationship("SaleItem", back_populates="product")


class SaleItem(Base):  # type: ignore[misc, valid-type]
    """Sale item model.

    Represents a product in a receipt."""

    __tablename__ = "sale_items"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    product = relationship("Product", back_populates="sale_items")
    quantity = Column(Float)
    total_price = Column(Float)
    receipt_id = Column(Integer, ForeignKey("receipts.id"))
    receipt = relationship("Receipt", back_populates="sale_items")


class Receipt(Base):  # type: ignore[misc, valid-type]
    """Receipt model.

    Represents a receipt in the system."""

    __tablename__ = "receipts"
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="receipts")
    payment_type = Column(String)
    payment_amount = Column(Float)
    total = Column(Float)
    change_given = Column(Float)
    sale_items = relationship("SaleItem", back_populates="receipt")

    def format_receipt(self, width: int = 40) -> str:
        """Format receipt for printing."""
        lines = ["ФОП Джонсонюк Борис Іванович ;)".center(width), "=" * width]

        total = 0
        for item in self.sale_items:
            item_total = item.quantity * item.product.price
            total += item_total
            line = "{:<30}".format(f"{item.quantity} x {item.product.price:,.0f}")
            lines.append(line)
            line = "{:<20}{:>20,.2f}".format(
                f"{item.product.name}", item_total
            ).replace(",", " ")
            lines.append(line)
            if len(self.sale_items) > 1:
                lines.append("-" * width)

        lines.extend(
            [
                "=" * width,
                "{:<10}{:>30,.2f}".format("СУМА", total).replace(",", " "),
                f"{self.payment_type.upper():<10}{self.payment_amount:>30,.2f}".replace(
                    ",", " "
                ),
                "{:<10}{:>30,.2f}".format("Решта", self.payment_amount - total).replace(
                    ",", " "
                ),
                "=" * width,
                f"Чек №{self.id}".center(width),
                f"{self.created_at.strftime('%d.%m.%Y %H:%M')}".center(width),
                "Дякуємо за покупку!".center(width),
                "=" * width,
            ]
        )
        return "\n".join(lines)


class ReceiptItem(Base):  # type: ignore[misc, valid-type]
    """Receipt item model.

    Represents a product in a receipt."""

    __tablename__ = "receipt_items"
    id = Column(Integer, primary_key=True)
    receipt_id = Column(Integer, ForeignKey("receipts.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Float)
    total_price = Column(Float)
    product = relationship("Product")
    receipt = relationship("Receipt", back_populates="items")


User.receipts = relationship("Receipt", order_by=Receipt.id, back_populates="user")
Receipt.items = relationship(
    "ReceiptItem", order_by=ReceiptItem.id, back_populates="receipt"
)


# This function is used to create tables in the database
def create_tables() -> None:
    """Create tables in the database."""
    from app.core.config import settings

    try:
        engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))
        Base.metadata.create_all(bind=engine)
        logger.info("Tables created successfully.")
    except Exception as e:
        logger.error(f"Failed to create tables: {e}")
