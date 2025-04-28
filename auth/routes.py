from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from fastapi_jwt_auth import AuthJWT
from passlib.context import CryptContext
from database import get_db, engine, SessionLocal
from models import User
from .schemas import UserSignupModel, UserLoginModel
from dependency import db_dependency
import datetime

router = APIRouter()

session = SessionLocal(bind=engine)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post('/signup', status_code=status.HTTP_201_CREATED)
async def user_signup(user_data: UserSignupModel, db: db_dependency):
    existing_user = db.query(User).filter(User.username == user_data.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this username already exists"
        )

    hashed_password = pwd_context.hash(user_data.password)

    new_user = User(
        username=user_data.username,
        password=hashed_password,
        is_admin=False
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    response_model = {
        'success': True,
        'code': 201,
        'message': 'User created successfully',
        'data': {
            'id': new_user.id,
            'username': new_user.username,
        }
    }
    return response_model


@router.post('/login', status_code=status.HTTP_200_OK)
async def user_login(user: UserLoginModel, Authorize: AuthJWT = Depends()):
    db_user = session.query(User).filter(User.username == user.username).first()

    if db_user and pwd_context.verify(user.password, db_user.password):
        access_lifetime = datetime.timedelta(minutes=60)
        refresh_lifetime = datetime.timedelta(days=1)

        access_token = Authorize.create_access_token(
            subject=db_user.username,
            expires_time=access_lifetime
        )
        refresh_token = Authorize.create_refresh_token(
            subject=db_user.username,
            expires_time=refresh_lifetime
        )

        response = {
            "success": True,
            "code": 200,
            "message": "User successfully logged in",
            "data": {
                "access": access_token,
                "refresh": refresh_token
            }
        }
        return jsonable_encoder(response)

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Invalid username or password"
    )


def verify_admin(user: User):
    """Check if the current user is an admin."""
    if not user or not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin users can perform this action"
        )


@router.put("/users/{id}/make-admin")
async def make_user_admin(
    id: int, 
    Authorize: AuthJWT = Depends(), 
    db: Session = Depends(get_db)
):
    try:
        Authorize.jwt_required()
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Enter valid token")
    
    current_user = Authorize.get_jwt_subject()
    admin_user = db.query(User).filter(User.username == current_user).first()

    verify_admin(admin_user)

    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    if user.is_admin:
        return jsonable_encoder({
            "success": False,
            "code": 400,
            "message": "User is already an admin"
        })
    
    user.is_admin = True
    db.commit()
    db.refresh(user)

    return jsonable_encoder({
        "success": True,
        "code": 200,
        "message": f"User {user.username} has been promoted to admin",
        "data": {
            "id": user.id,
            "username": user.username,
            "is_admin": user.is_admin
        }
    })
