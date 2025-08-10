# app/controller/note_controller.py
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from app.configuration.database import get_db
from app.model.note_model import Note
from app.schema.note_schema import NoteCreate, NoteOut
from app.service.note_service import get_user_notes, add_note, edit_note, remove_note
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from app.configuration.security import SECRET_KEY, ALGORITHM
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/notes", tags=["notes"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user_id(token: str = Depends(oauth2_scheme)):
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

@router.get("/", response_model=list[NoteOut])
def read_notes(user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    return get_user_notes(db, user_id)

@router.post("/", response_model=NoteOut)
def create_note(note: NoteCreate, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    return add_note(db, user_id, note)

@router.put("/{note_id}", response_model=NoteOut)
def update_note(note_id: str, note: NoteCreate, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    updated = edit_note(db, note_id, note, user_id)
    if not updated:
        raise HTTPException(status_code=404, detail="Note not found")
    return updated

@router.delete("/{note_id}")
def delete_note(note_id: str, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    existing = db.query(Note).filter(Note.id == note_id, Note.id_user == user_id).first()
    if not existing:
        raise HTTPException(status_code=404, detail="Note not found")
    remove_note(db, note_id)
    return {"detail": "Note deleted"}

@router.delete("/", response_class=JSONResponse, tags=["notes"])
def delete_notes_by_ids(
    ids: List[str] = Body(..., embed=True, description="List of note IDs to delete"),
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    notes = db.query(Note).filter(Note.id.in_(ids), Note.id_user == user_id).all()
    if len(notes) != len(ids):
        raise HTTPException(status_code=404, detail="Some notes not found or do not belong to the user")

    for note in notes:

        db.delete(note)
    db.commit()

    return {"detail": f"{len(notes)} notes deleted"}
