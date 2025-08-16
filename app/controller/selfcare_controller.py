# app/controller/selfcare_controller.py
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.configuration.database import get_db
from app.schema.selfcare_schema import SelfCareCreate, SelfCareOut
from app.service.selfcare_service import save_or_update_selfcare, get_selfcare_by_user, update_selfcare, delete_selfcare

router = APIRouter(prefix="/selfcare", tags=["selfcare"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
db: Session = Depends(get_db)


def get_current_user_id(token: str = Depends(oauth2_scheme)):
    from app.configuration.security import SECRET_KEY, ALGORITHM
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_email: str = payload.get("sub")
        if user_email is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        from app.repository.user_repository import get_user_by_email
        db = next(get_db())
        user = get_user_by_email(db, user_email)
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        return user.id
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@router.get("/", response_model=list[SelfCareOut])
def read_selfcare(user_id: str = Depends(get_current_user_id), db: Session = Depends(get_db)):
    return get_selfcare_by_user(db, user_id)

@router.post("/", response_model=SelfCareOut)
def create_selfcare(selfcare: SelfCareCreate, user_id: str = Depends(get_current_user_id), db: Session = Depends(get_db)):
    return save_or_update_selfcare(db, user_id, selfcare)

@router.put("/{selfcare_id}", response_model=SelfCareOut)
def update_selfcare_entry(selfcare_id: str, selfcare: SelfCareCreate, user_id: str = Depends(get_current_user_id), db: Session = Depends(get_db)):
    updated = update_selfcare(db, selfcare_id, selfcare, user_id)
    if not updated:
        raise HTTPException(status_code=404, detail="SelfCare entry not found")
    return updated


@router.delete("/{selfcare_id}")
def delete_selfcare_entry(selfcare_id: str, user_id: str = Depends(get_current_user_id), db: Session = Depends(get_db)):
    deleted = delete_selfcare(db, selfcare_id, user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="SelfCare entry not found")
    return {"message": "SelfCare entry deleted successfully"}
# /