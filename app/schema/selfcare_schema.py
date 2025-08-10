# app/schema/selfcare_schema.py
from pydantic import BaseModel
from typing import List, Optional

class SelfCareBase(BaseModel):
    date: str
    mood: str
    emotions: List[str]
    activities: List[str]

class SelfCareCreate(SelfCareBase):
    id: Optional[str]  # Можно передавать или генерить на сервере
    id_user: int

class SelfCareOut(SelfCareBase):
    id: str
    id_user: int

    class Config:
        orm_mode = True
