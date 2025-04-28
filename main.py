from fastapi import FastAPI
from fastapi_jwt_auth import AuthJWT
from pydantic import BaseModel
from config import settings
from database import Base, engine
from auth.routes import router as auth_router
from admin.routes import router as admin_router
from customer.routes import router as customer_router

Base.metadata.create_all(bind=engine)

class JWTSettings(BaseModel):
    authjwt_secret_key: str = settings.JWT_SECRET_KEY
    authjwt_algorithm: str = settings.JWT_ALGORITHM

@AuthJWT.load_config
def get_config():
    return JWTSettings()

app = FastAPI()

app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(admin_router, prefix="/admin", tags=["Admin Routes"])   
app.include_router(customer_router, prefix="/customer", tags=["Customer Routes"])

















