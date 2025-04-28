from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from fastapi_jwt_auth import AuthJWT
from models import Product, Order, User
from database import get_db
from .schemas import ProductCreate, ProductUpdate

router = APIRouter()

def verify_admin(user: User):
    if not user or not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin users can perform this action"
        )


@router.post("/add-product")
async def create_product(
    product_data: ProductCreate, 
    Authorize: AuthJWT = Depends(), 
    db: Session = Depends(get_db)
):
    try:
        Authorize.jwt_required()
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Enter valid token")
    
    current_user = Authorize.get_jwt_subject()
    user = db.query(User).filter(User.username == current_user).first()

    if user:
        verify_admin(user)
        new_product = Product(
            name=product_data.name,
            description=product_data.description,
            price=product_data.price,
            stock=product_data.stock,
            category=product_data.category
        )
        db.add(new_product)
        db.commit()
        db.refresh(new_product)
        return jsonable_encoder({
            "success": True,
            "code": 201,
            "message": "Product added successfull y",
            "data": new_product
        })
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid user")


@router.get("/get-products")
async def get_all_products(Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    """
    Retrieve all products from the database.
    Only accessible to admin users.
    """
    try:
        Authorize.jwt_required()
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Enter valid token")
    
    current_user = Authorize.get_jwt_subject()
    user = db.query(User).filter(User.username == current_user).first()

    verify_admin(user)

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



@router.get("/get-product/{id}")
async def get_product(id: int, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    try:
        Authorize.jwt_required()
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Enter valid token")
    
    current_user = Authorize.get_jwt_subject()
    user = db.query(User).filter(User.username == current_user).first()

    if user:
        verify_admin(user)
        product = db.query(Product).filter(Product.id == id).first()
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
        return jsonable_encoder({
            "success": True,
            "code": 200,
            "data": product
        })
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid user")


@router.put("/update-product/{id}")
async def update_product(
    id: int, 
    product_data: ProductUpdate, 
    Authorize: AuthJWT = Depends(), 
    db: Session = Depends(get_db)
):
    try:
        Authorize.jwt_required()
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Enter valid token")
    
    current_user = Authorize.get_jwt_subject()
    user = db.query(User).filter(User.username == current_user).first()

    if user:
        verify_admin(user)
        product = db.query(Product).filter(Product.id == id).first()
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
        
        for key, value in product_data.dict(exclude_unset=True).items():
            setattr(product, key, value)
        db.commit()
        db.refresh(product)
        return jsonable_encoder({
            "success": True,
            "code": 200,
            "message": "Product updated successfully",
            "data": product
        })
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid user")


@router.delete("/delete-product/{id}")
async def delete_product(id: int, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    try:
        Authorize.jwt_required()
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Enter valid token")
    
    current_user = Authorize.get_jwt_subject()
    user = db.query(User).filter(User.username == current_user).first()

    if user:
        verify_admin(user)
        product = db.query(Product).filter(Product.id == id).first()
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
        db.delete(product)
        db.commit()
        return jsonable_encoder({
            "success": True,
            "code": 200,
            "message": "Product deleted successfully"
        })
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid user")


@router.get("/orders")
async def list_orders(Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    try:
        Authorize.jwt_required()
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Enter valid token")
    
    current_user = Authorize.get_jwt_subject()
    user = db.query(User).filter(User.username == current_user).first()

    if user:
        verify_admin(user)
        orders = db.query(Order).all()
        return jsonable_encoder({
            "success": True,
            "code": 200,
            "data": orders
        })
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid user")


@router.get("/get-order/{id}")
async def get_order(id: int, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    try:
        Authorize.jwt_required()
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Enter valid token")
    
    current_user = Authorize.get_jwt_subject()
    user = db.query(User).filter(User.username == current_user).first()

    if user:
        verify_admin(user)
        order = db.query(Order).filter(Order.id == id).first()
        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
        return jsonable_encoder({
            "success": True,
            "code": 200,
            "data": order
        })
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid user")