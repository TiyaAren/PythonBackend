from fastapi import FastAPI
from app.model import user_model  # важно, чтобы таблица создалась
from app.configuration.database import engine
from app.controller import auth_controller

user_model.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth_controller.router)
