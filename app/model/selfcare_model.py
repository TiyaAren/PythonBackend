# app/model/selfcare_model.py
from sqlalchemy import Column, String, Integer, ARRAY
from app.configuration.database import Base

class SelfCare(Base):
    __tablename__ = "selfcare"

    id = Column(String, primary_key=True, index=True)  # UUID в строке
    id_user = Column(Integer, nullable=False)
    date = Column(String, nullable=False)
    mood = Column(String, nullable=False)
    emotions = Column(ARRAY(String))
    activities = Column(ARRAY(String))
