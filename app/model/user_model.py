from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from app.configuration.database import Base

class User(Base):
    __tablename__ = "users"
    # jjj
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
