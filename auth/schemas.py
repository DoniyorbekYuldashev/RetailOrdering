from pydantic import BaseModel


class UserSignupModel(BaseModel):
    username: str
    password: str


class UserLoginModel(BaseModel):
    username: str
    password: str
