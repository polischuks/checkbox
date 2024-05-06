from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud
from app import logger as log
from app import schemas
from app.dependencies import get_current_user, get_db
from app.models import Receipt, User

logger = log.get_logger()

router = APIRouter()


@router.post("/receipts/", response_model=schemas.ReceiptResponse)
def create_receipt(
    receipt: schemas.ReceiptCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> schemas.ReceiptResponse:
    """Create a new receipt in the database.

    Args:
        receipt (schemas.ReceiptCreate): Receipt data.
        db (Session): Database session.
        user (User): User data.

    Returns:
        schemas.ReceiptResponse: Receipt data.
    """
    return crud.create_receipt(db=db, receipt=receipt, user=user)


@router.get("/receipts/", response_model=list[schemas.Receipt])
def read_receipts(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
    date_from: datetime | None = None,
    date_to: datetime | None = None,
    min_total: float | None = None,
    payment_type: str | None = None,
    skip: int = 0,
    limit: int = 10,
) -> list[schemas.Receipt]:
    """Get receipts by user id. Optionally filter by date, total, and payment type.

    Args:
        db (Session): Database session.
        user (User): User id.
        date_from (Optional[datetime], optional): Filter by date from. Defaults to None.
        date_to (Optional[datetime], optional): Filter by date to. Defaults to None.
        min_total (Optional[float], optional): Filter by minimum total. Defaults to None.
        payment_type (Optional[str], optional): Filter by payment type. Defaults to None.
        skip (int, optional): Skip records. Defaults to 0.
        limit (int, optional): Limit records. Defaults to 10.

    Returns:
        List[Receipt]: List of receipts.
    """
    query = crud.get_receipts_by_user(db=db, user_id=user.id)

    if date_from:
        query = query.filter(Receipt.created_at >= date_from)
    if date_to:
        query = query.filter(Receipt.created_at <= date_to)
    if min_total:
        query = query.filter(Receipt.total >= min_total)
    if payment_type:
        query = query.filter(Receipt.payment_type == payment_type)

    receipts = query.offset(skip).limit(limit).all()
    return receipts


@router.get("/receipts/{receipt_id}/", response_model=schemas.Receipt)
def read_receipt(
    receipt_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> schemas.Receipt | None:
    """Get a receipt by user id and receipt id.

    Args:
        receipt_id (int): Receipt id.
        db (Session): Database session.
        user (User): User id.

    Returns:
        ReceiptResponse: Receipt data.
    """
    receipt = crud.get_receipt_by_user_and_id(
        db=db, receipt_id=receipt_id, user_id=user.id
    )
    if not receipt:
        raise HTTPException(status_code=404, detail="Receipt not found")
    return receipt


@router.get("/receipts/public/{receipt_id}", response_model=schemas.Receipt)
def get_receipt_public(
    receipt_id: int, db: Session = Depends(get_db)
) -> schemas.Receipt:
    """Get a receipt by id.

    Args:
        receipt_id (int): Receipt id.
        db (Session): Database session.

    Returns:
        schemas.Receipt: Receipt data.
    """
    receipt = crud.get_receipt_by_id(db=db, receipt_id=receipt_id)
    if not receipt:
        raise HTTPException(status_code=404, detail="Receipt not found")
    return receipt


@router.get("/receipts/{receipt_id}/text")
def get_receipt_text(receipt_id: int, db: Session = Depends(get_db)) -> str:
    """Get a receipt text by id.

    Args:
        receipt_id (int): Receipt id.
        db (Session): Database session.

    Returns:
        str: Receipt text.
    """
    receipt = crud.get_receipt_by_id(db=db, receipt_id=receipt_id)
    if not receipt:
        raise HTTPException(status_code=404, detail="Receipt not found")
    logger.info(f"receipt text format:\n\n{receipt.format_receipt()}")
    return receipt.format_receipt()
