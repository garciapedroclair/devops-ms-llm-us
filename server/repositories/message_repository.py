from sqlalchemy.orm import Session
from models import Message

def create_message(db: Session, content: str) -> Message:
    message = Message(content=content)
    db.add(message)
    db.commit()
    db.refresh(message)
    return message

def list_messages(db: Session) -> list[Message]:
    return db.query(Message).order_by(Message.created_at.desc()).all()
