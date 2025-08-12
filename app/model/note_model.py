# app/model/note_model.py
from sqlalchemy import Column, String, Integer
from app.configuration.database import Base

class Note(Base):
    __tablename__ = "notes"

    id = Column(String, primary_key=True, index=True)  # UUID в строке
    id_user = Column(String, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    date = Column(String, nullable=False)
