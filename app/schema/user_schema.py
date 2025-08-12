from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    name: str = Field(..., min_length=1)
    email: EmailStr
    password: str = Field(..., min_length=6)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    id_user: str
    name: str


class UserOut(BaseModel):
    id: str
    name: str
    email: EmailStr

    class Config:
        orm_mode = True
