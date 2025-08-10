from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.configuration.database import SessionLocal, get_db
from app.configuration.security import create_access_token
from app.service.user_service import register_user, login_user
from app.schema.user_schema import UserCreate, UserLogin, UserOut, LoginResponse

router = APIRouter(prefix="/auth", tags=["auth"])

db: Session = Depends(get_db)


@router.post("/register", response_model=UserOut)
def register(user: UserCreate, db: Session = Depends(get_db)):
    try:
        new_user = register_user(db, user)
        return new_user
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login", response_model=LoginResponse)
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = login_user(db, user.email, user.password)
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": db_user.email})
    return LoginResponse(
        access_token=token,
        token_type="bearer",
        id_user=db_user.id,
        name=db_user.name
    )