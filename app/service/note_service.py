# app/service/note_service.py

import uuid
from sqlalchemy.orm import Session
from app.model.note_model import Note
from app.schema.note_schema import NoteCreate


def get_user_notes(db: Session, user_id: str):
    return db.query(Note).filter(Note.id_user == user_id).all()

def add_note(db: Session, user_id: str, note: NoteCreate):
    new_id = note.id or str(uuid.uuid4())
    new_note = Note(
        id=new_id,
        id_user=user_id,
        title=note.title,
        content=note.content,
        date=note.date
    )
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note

def edit_note(db: Session, note_id: str, note_data: NoteCreate, user_id: str):
    existing = db.query(Note).filter(Note.id == note_id, Note.id_user == user_id).first()
    if not existing:
        return None
    existing.title = note_data.title
    existing.content = note_data.content
    existing.date = note_data.date
    db.commit()
    db.refresh(existing)
    return existing

def remove_note(db: Session, note_id: str):
    note = db.query(Note).filter(Note.id == note_id).first()
    if note:
        db.delete(note)
        db.commit()
