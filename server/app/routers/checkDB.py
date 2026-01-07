from fastapi import APIRouter
from sqlalchemy import text
from ..utils.db import SessionLocal

router = APIRouter()

@router.get("/health")
def health_check():
    db = SessionLocal()
    result = db.execute(text("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """))
    tables = [row[0] for row in result.fetchall()]
    db.close()
    return {"tables": tables}

@router.get("/participants")
def list_participants_atributes():
    db = SessionLocal()
    query = db.execute(text("Select * From participant"))
    columns =  query.keys()
    data = [dict(zip(columns, row)) for row in query.fetchall()]
    return data

@router.get("/tasks")
def list_tasks_attributes():
    db = SessionLocal()
    query = db.execute(text("SELECT * FROM task"))
    columns = query.keys()
    data = [dict(zip(columns, row)) for row in query.fetchall()]
    db.close()
    return data
