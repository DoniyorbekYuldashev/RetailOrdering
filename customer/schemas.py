from pydantic import BaseModel
from typing import List, Optional


class ProductSchema(BaseModel):
    id: int
    name: str
    description: Optional[str]
    price: float
    stock: int
    category: Optional[str]

    class Config:
        orm_mode = True


class OrderItem(BaseModel):
    product_id: int
    quantity: int


class OrderCreate(BaseModel):
    items: List[OrderItem]


class OrderSchema(BaseModel):
    id: int
    user_id: int
    total_amount: float
    status: str
    order_date: str

    class Config:
        orm_mode = True
