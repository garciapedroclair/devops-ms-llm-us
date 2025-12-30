from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from dotenv import load_dotenv

from database import engine
from dependencies import get_db
from models import Base
from repositories.message_repository import (
    create_message,
    list_messages
)
from schemas.message import (
    MessageCreate,
    MessageResponse
)

load_dotenv()

app = FastAPI(title="Message Microservice")

# DEV ONLY: create tables automatically
Base.metadata.create_all(bind=engine)

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/messages", response_model=MessageResponse)
def create_message_endpoint(
    payload: MessageCreate,
    db: Session = Depends(get_db)
):
    return create_message(db, payload.content)

@app.get("/messages", response_model=list[MessageResponse])
def list_messages_endpoint(
    db: Session = Depends(get_db)
):
    return list_messages(db)
