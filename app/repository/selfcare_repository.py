# app/repository/selfcare_repository.py
from sqlalchemy.orm import Session
from app.model.selfcare_model import SelfCare
from app.schema.selfcare_schema import SelfCareCreate
from datetime import datetime

import json

def get_selfcare_by_user_date(db: Session, user_id: int, date: datetime.date):
    return db.query(SelfCare).filter(SelfCare.user_id == user_id, SelfCare.date == date).first()

def create_selfcare(db: Session, user_id: int, selfcare: SelfCareCreate):
    emotions_str = json.dumps(selfcare.emotions or [])
    activities_str = json.dumps(selfcare.activities or [])
    db_selfcare = SelfCare(
        user_id=user_id,
        date=selfcare.date,
        mood=selfcare.mood,
        emotions=emotions_str,
        activities=activities_str
    )
    db.add(db_selfcare)
    db.commit()
    db.refresh(db_selfcare)
    return db_selfcare

def update_selfcare(db: Session, existing_selfcare: SelfCare, selfcare: SelfCareCreate):
    import json
    existing_selfcare.mood = selfcare.mood
    existing_selfcare.emotions = json.dumps(selfcare.emotions or [])
    existing_selfcare.activities = json.dumps(selfcare.activities or [])
    db.commit()
    db.refresh(existing_selfcare)
    return existing_selfcare
