from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from fastapi_jwt_auth import AuthJWT
from passlib.context import CryptContext
from database import get_db, engine, SessionLocal
from models import User, Product, Order, OrderDetail
from .schemas import OrderCreate
from dependency import db_dependency
import datetime
    
router = APIRouter()

session = SessionLocal(bind=engine)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.get("/products")
async def get_all_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    if not products:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No products found")

    return jsonable_encoder({
        "success": True,
        "code": 200,
        "message": "Products retrieved successfully",
        "data": [
            {
                "id": product.id,
                "name": product.name,
                "description": product.description,
                "price": product.price,
                "stock": product.stock,
                "category": product.category,
                "created_at": product.created_at,
                "updated_at": product.updated_at
            }
            for product in products
        ]
    })


@router.post("/make-order")
async def create_order(
    order_data: OrderCreate, 
    Authorize: AuthJWT = Depends(), 
    db: Session = Depends(get_db)
):
    try:
        Authorize.jwt_required()
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Enter valid token")
    
    current_user = Authorize.get_jwt_subject()
    user = db.query(User).filter(User.username == current_user).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid user")

    total_amount = 0
    for item in order_data.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with id {item.product_id} not found"
            )
        if product.stock < item.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Not enough stock for product {product.name}"
            )
        total_amount += product.price * item.quantity

    new_order = Order(
        user_id=user.id,
        total_amount=total_amount,
        status="pending"
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    for item in order_data.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        order_detail = OrderDetail(
            order_id=new_order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            total_price=product.price * item.quantity
        )
        product.stock -= item.quantity
        db.add(order_detail)

    db.commit()

    return jsonable_encoder({
        "success": True,
        "code": 201,
        "message": "Order created successfully",
        "data": {
            "order_id": new_order.id,
            "total_amount": new_order.total_amount,
            "status": new_order.status
        }
    })


@router.get("/get-order/{customerId}")
async def get_customer_orders(customerId: int, db: Session = Depends(get_db)):
    orders = db.query(Order).filter(Order.user_id == customerId).all()
    if not orders:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No orders found for this customer")

    return jsonable_encoder({
        "success": True,
        "code": 200,
        "message": "Customer orders retrieved successfully",
        "data": [
            {
                "id": order.id,
                "total_amount": order.total_amount,
                "status": order.status,
                "order_date": order.order_date,
                "created_at": order.created_at,
                "updated_at": order.updated_at
            }
            for order in orders
        ]
    })


@router.get("/get-order/{orderId}/status")
async def get_order_status(orderId: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == orderId).first()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

    return jsonable_encoder({
        "success": True,
        "code": 200,
        "message": "Order status retrieved successfully",
        "data": {
            "order_id": order.id,
            "status": order.status
        }
    })
