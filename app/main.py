# app/main.py

from fastapi import FastAPI
from app.controller import auth_controller
from app.configuration.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth_controller.router)
