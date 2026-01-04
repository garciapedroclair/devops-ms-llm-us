import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

app = FastAPI(title="LLM for US Microservice")

origins = [
    "http://localhost:3001",  # React dev server
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

@app.get("/tasks/stats_time_llm")
def get_task_stats():
    db = SessionLocal()
    query = db.execute(text("SELECT time, llm FROM task"))
    columns = query.keys()
    data = [dict(zip(columns, row)) for row in query.fetchall()]
    db.close()
    return {
            "time_llm_true": [d["time"] for d in data if d["llm"]],
            "time_llm_false": [d["time"] for d in data if not d["llm"]]
        }

@app.get("/llm_us/knowledge")
def list_knowledge():
    db = SessionLocal()
    sql = """
        SELECT 
            code, 
            prog_oo, 
            soft_arch, 
            web_tech, 
            db_systems, 
            sw_project_mgmt, 
            requirements, 
            agile_methods, 
            llm_usage 
        FROM participant
    """
    query = db.execute(text(sql))
    # Mapeia as colunas para o formato de dicionário que o Next.js espera
    columns = query.keys()
    data = [dict(zip(columns, row)) for row in query.fetchall()]
    db.close()
    return data

@app.get("/llm_us/knowledge/heatmap")
def get_knowledge_heatmap():
    db = SessionLocal()
    # Lista de colunas de conhecimento
    areas = [
        "prog_oo", "soft_arch", "web_tech", "db_systems", 
        "sw_project_mgmt", "requirements", "agile_methods", "llm_usage"
    ]
    
    query = db.execute(text(f"SELECT {', '.join(areas)} FROM participant"))
    rows = query.fetchall()
    db.close()

    total = len(rows)
    if total == 0: return []

    result = []
    for area in areas:
        # Conta frequência de cada nível (1-5) para esta área
        counts = { "1": 0, "2": 0, "3": 0, "4": 0, "5": 0 }
        for row in rows:
            val = str(getattr(row, area))
            if val in counts:
                counts[val] += 1
        
        # Converte para percentual
        levels_percent = { k: round((v / total) * 100, 1) for k, v in counts.items() }
        result.append({ "knowledge": area, "levels": levels_percent })

    return result

@app.get("/llm_us/sankey/positive")
def get_positive_sankey():
    return {
        "type": "positive",
        "description": "Positive perceptions of LLM usage grouped by dimension and category",
        "nodes": [
            {"name": "Time"}, {"name": "Quality"}, {"name": "Speed"},
            {"name": "Agility"}, {"name": "Precision"}, {"name": "Ease of Use"},
            {"name": "Creativity & Ideas"}, {"name": "Clarity"},
            {"name": "Standardization"}, {"name": "Context"}
        ],
        "links": [
            { "source": "Time", "target": "Speed", "value": 17 },
            { "source": "Time", "target": "Agility", "value": 8 },
            { "source": "Time", "target": "Precision", "value": 7 },
            { "source": "Quality", "target": "Ease of Use", "value": 6 },
            { "source": "Quality", "target": "Creativity & Ideas", "value": 11 },
            { "source": "Quality", "target": "Clarity", "value": 7 },
            { "source": "Quality", "target": "Standardization", "value": 3 },
            { "source": "Quality", "target": "Context", "value": 2 }
        ]
    }

@app.get("/llm_us/sankey/negative")
def get_negative_sankey():
    return {
        "type": "negative",
        "description": "Negative perceptions of LLM usage grouped by dimension and category",
        "nodes": [
            {"name": "Learning"}, {"name": "Reliability"}, {"name": "Overdependence"},
            {"name": "Reduced Learning"}, {"name": "Loss of Critical Thinking"},
            {"name": "Loss of Personal Authorship"}, {"name": "Generic Output"},
            {"name": "Inaccurate"}, {"name": "Misinterpretation"},
            {"name": "Misalignment"}
        ],
        "links": [
            { "source": "Learning", "target": "Overdependence", "value": 9 },
            { "source": "Learning", "target": "Reduced Learning", "value": 7 },
            { "source": "Learning", "target": "Loss of Critical Thinking", "value": 6 },
            { "source": "Learning", "target": "Loss of Personal Authorship", "value": 4 },
            { "source": "Reliability", "target": "Generic Output", "value": 8 },
            { "source": "Reliability", "target": "Inaccurate", "value": 6 },
            { "source": "Reliability", "target": "Misinterpretation", "value": 5 },
            { "source": "Reliability", "target": "Misalignment", "value": 3 }
        ]
    }