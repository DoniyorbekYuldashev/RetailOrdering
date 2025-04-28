from pydantic import BaseModel
from typing import Optional


class ProductBase(BaseModel):
    name: str
    description: Optional[str]
    price: float
    stock: int
    category: Optional[str]


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    price: Optional[float]
    stock: Optional[int]
    category: Optional[str]


class OrderBase(BaseModel):
    user_id: int
    total_amount: float
    status: Optional[str]


class OrderDetailBase(BaseModel):
    order_id: int
    product_id: int
    quantity: int
    total_price: float
