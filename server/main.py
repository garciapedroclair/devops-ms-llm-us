import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

app = FastAPI(title="Message Microservice")

origins = [
    "http://localhost:5173",  # React dev server
]

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
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

@app.get("/participants")
def list_participants_atributes():
    db = SessionLocal()
    query = db.execute(text("Select * From participant"))
    columns =  query.keys()
    data = [dict(zip(columns, row)) for row in query.fetchall()]
    return data

@app.get("/tasks")
def list_tasks_attributes():
    db = SessionLocal()
    query = db.execute(text("SELECT * FROM task"))
    columns = query.keys()
    data = [dict(zip(columns, row)) for row in query.fetchall()]
    db.close()
    return data

