from datetime import datetime
from typing import List

from pydantic import BaseModel


class UserCreate(BaseModel):
    name: str
    username: str
    password: str


class User(BaseModel):
    id: int
    name: str
    username: str

    class Config:
        orm_mode = True


class SaleItemCreate(BaseModel):
    product_id: int
    quantity: float


class ReceiptCreate(BaseModel):
    user_id: int
    sale_items: List[SaleItemCreate]
    payment_type: str
    payment_amount: float


class Receipt(BaseModel):
    id: int
    created_at: datetime
    user_id: int
    payment_type: str
    payment_amount: float
    total: float
    sale_items: List[SaleItemCreate]

    class Config:
        orm_mode = True


class SaleItemResponse(BaseModel):
    product_name: str
    quantity: float
    total_price: float


class ReceiptResponse(BaseModel):
    id: int
    created_at: datetime
    total: float
    payment_type: str
    payment_amount: float
    change_given: float
    items: List[SaleItemResponse]

    class Config:
        orm_mode = True
