# app/service/auth_service.py

from sqlalchemy.orm import Session
from app.schema.user_schema import UserCreate
from app.model.user_model import User
from app.repository import user_repository
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def register_user(user_data: UserCreate, db: Session):
    existing_user = user_repository.get_user_by_email(db, user_data.email)
    if existing_user:
        raise Exception("Email already registered")
    hashed_pw = pwd_context.hash(user_data.password)
    new_user = User(name=user_data.name, email=user_data.email, hashed_password=hashed_pw)
    return user_repository.create_user(db, new_user)

def verify_user(email: str, password: str, db: Session):
    user = user_repository.get_user_by_email(db, email)
    if not user or not pwd_context.verify(password, user.hashed_password):
        return None
    return user
