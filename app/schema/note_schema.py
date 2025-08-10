# app/schema/note_schema.py
from pydantic import BaseModel
from datetime import datetime

from pydantic import BaseModel
from typing import Optional

class NoteBase(BaseModel):
    title: str
    content: str
    date: str

class NoteCreate(NoteBase):
    id: Optional[str]
    id_user: int

class NoteOut(NoteBase):
    id: str
    id_user: int

    class Config:
        orm_mode = True
