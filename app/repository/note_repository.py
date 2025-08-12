# app/repository/note_repository.py
from sqlalchemy.orm import Session
from app.model.note_model import Note
from app.schema.note_schema import NoteCreate

def get_notes_by_user(db: Session, user_id: str):
    return db.query(Note).filter(Note.user_id == user_id).all()

def create_note(db: Session, user_id: str, note: NoteCreate):
    db_note = Note(user_id=user_id, content=note.content)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

def update_note(db: Session, note_id: str, content: str):
    note = db.query(Note).filter(Note.id == note_id).first()
    if note:
        note.content = content
        db.commit()
        db.refresh(note)
    return note

def delete_note(db: Session, note_id: str):
    note = db.query(Note).filter(Note.id == note_id).first()
    if note:
        db.delete(note)
        db.commit()
    return note
