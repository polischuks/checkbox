from passlib.context import CryptContext
from sqlalchemy.orm import Query, Session

from .models import Product, Receipt, SaleItem, User
from .schemas import ReceiptCreate, UserCreate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user_by_username(db: Session, username: str) -> User | None:
    """Get user by username

    Args:
        db (Session): SQLAlchemy session
        username (str): Username
    """
    return db.query(User).filter(User.username == username).first()


def create_user(db: Session, user: UserCreate) -> User:
    """Create a new user in the database

    Args:
        db (Session): SQLAlchemy session
        user (UserCreate): UserCreate schema
    """
    hashed_password = pwd_context.hash(user.password)
    db_user = User(
        name=user.name, username=user.username, hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_receipts_by_user(db: Session, user_id: int) -> Query[Receipt]:
    """Get receipts by user id

    Args:
        db (Session): SQLAlchemy session
        user_id (int): User id
    """
    return db.query(Receipt).filter(Receipt.user_id == user_id)


def get_receipt_by_user_and_id(
    db: Session, receipt_id: int, user_id: int
) -> Receipt | None:
    """Get receipt by user id and receipt id

    Args:
        db (Session): SQLAlchemy session
        receipt_id (int): Receipt id
        user_id (int): User id
    """
    return (
        db.query(Receipt)
        .filter(Receipt.id == receipt_id, Receipt.user_id == user_id)
        .first()
    )


def create_receipt(db: Session, receipt: ReceiptCreate, user: User) -> Receipt:
    """Create a new receipt in the database
    and add sale items to the receipt

    Args:
        db (Session): SQLAlchemy session
        receipt (ReceiptCreate): ReceiptCreate schema
        user (User): User model
    """
    new_receipt = Receipt(
        user_id=user.id,
        payment_type=receipt.payment_type,
        payment_amount=receipt.payment_amount,
        total=0,  # Initialize total to zero; it will be calculated based on sale items
        change_given=0,  # Initialize change given, will be updated later
    )
    db.add(new_receipt)
    db.flush()

    total = 0
    for item_data in receipt.sale_items:
        product = db.query(Product).filter(Product.id == item_data.product_id).first()
        if product:
            total_price = product.price * item_data.quantity
            sale_item = SaleItem(
                product_id=product.id,
                quantity=item_data.quantity,
                total_price=total_price,
                receipt=new_receipt,
            )
            db.add(sale_item)
            total += total_price  # Update total as each item is added

    # Update total and change given after all items are added
    new_receipt.total = total
    new_receipt.change_given = new_receipt.payment_amount - total

    db.commit()
    db.refresh(new_receipt)
    return new_receipt


def get_receipt_by_id(db: Session, receipt_id: int) -> Receipt | None:
    """Get receipt by id

    Args:
        db (Session): SQLAlchemy session
        receipt_id (int): Receipt id
    """
    return db.query(Receipt).filter(Receipt.id == receipt_id).first()
