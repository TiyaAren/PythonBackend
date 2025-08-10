# app/service/selfcare_service.py
import uuid
from sqlalchemy.orm import Session
from app.model.selfcare_model import SelfCare
from app.schema.selfcare_schema import SelfCareCreate

def save_or_update_selfcare(db: Session, user_id: int, selfcare: SelfCareCreate):
    existing = db.query(SelfCare).filter(SelfCare.id_user == user_id, SelfCare.date == selfcare.date).first()
    if existing:
        # Обновляем
        existing.mood = selfcare.mood
        existing.emotions = selfcare.emotions
        existing.activities = selfcare.activities
        db.commit()
        db.refresh(existing)
        return existing
    else:
        # Создаем
        new_id = selfcare.id or str(uuid.uuid4())
        new_selfcare = SelfCare(
            id=new_id,
            id_user=user_id,
            date=selfcare.date,
            mood=selfcare.mood,
            emotions=selfcare.emotions,
            activities=selfcare.activities
        )
        db.add(new_selfcare)
        db.commit()
        db.refresh(new_selfcare)
        return new_selfcare

def get_selfcare_by_user(db: Session, user_id: int):
    return db.query(SelfCare).filter(SelfCare.id_user == user_id).all()

def update_selfcare(db: Session, selfcare_id: str, selfcare: SelfCareCreate, user_id: int):
    existing = db.query(SelfCare).filter(SelfCare.id == selfcare_id, SelfCare.id_user == user_id).first()
    if not existing:
        return None
    existing.date = selfcare.date
    existing.mood = selfcare.mood
    existing.emotions = selfcare.emotions
    existing.activities = selfcare.activities
    db.commit()
    db.refresh(existing)
    return existing
