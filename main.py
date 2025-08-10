from fastapi import FastAPI

from app.configuration.database import engine
from app.controller import auth_controller, selfcare_controller, note_controller
from app.model import user_model, selfcare_model, note_model

user_model.Base.metadata.create_all(bind=engine)
selfcare_model.Base.metadata.create_all(bind=engine)
note_model.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth_controller.router)
app.include_router(selfcare_controller.router)
app.include_router(note_controller.router)
