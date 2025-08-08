from sqlalchemy.orm import Session
from app.repository import user_repository
from app.schema.user_schema import UserCreate
from app.configuration.security import verify_password

def register_user(db: Session, user: UserCreate):
    existing = user_repository.get_user_by_email(db, user.email)
    if existing:
        raise Exception("User already exists")
    return user_repository.create_user(db, user)

def login_user(db: Session, email: str, password: str):
    user = user_repository.get_user_by_email(db, email)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user
