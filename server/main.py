import os
from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import requests

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


def median(values):
    n = len(values)
    if n == 0:
        return 0

    values = sorted(values)
    mid = n // 2

    if n % 2 == 0:
        return (values[mid - 1] + values[mid]) / 2
    else:
        return values[mid]


def quartiles(values):
    if not values:
        return [0, 0, 0, 0, 0]

    values = sorted(values)
    n = len(values)

    q2 = median(values)
    lower_half = values[: n // 2]
    upper_half = values[(n + 1) // 2 :]

    q1 = median(lower_half)
    q3 = median(upper_half)

    return [
        values[0],   # min
        q1,          # q1
        q2,          # median
        q3,          # q3
        values[-1],  # max
    ]


@app.get("/tasks/stats_time_llm")
def get_task_stats():
    db = SessionLocal()

    query = db.execute(text("SELECT time, llm FROM task"))
    rows = query.fetchall()

    db.close()

    time_llm_true = [row.time for row in rows if row.llm]
    time_llm_false = [row.time for row in rows if not row.llm]

    return {
        "labels": ["With LLM", "Without LLM"],
        "boxplot": [
            quartiles(time_llm_true),
            quartiles(time_llm_false),
        ],
        "count": {
            "with_llm": len(time_llm_true),
            "without_llm": len(time_llm_false),
        },
    }

@app.get("/tasks/stats_group_time")
def get_group_time_stats():
    db = SessionLocal()

    query = db.execute(text("SELECT time, \"group\" FROM task"))
    rows = query.fetchall()

    db.close()

    group_01 = [row.time for row in rows if row.group == "G1"]
    group_02 = [row.time for row in rows if row.group == "G2"]

    return {
        "labels": ["G1", "G2"],
        "boxplot": [
            quartiles(group_01),
            quartiles(group_02),
        ],
        "count": {
            "G1": len(group_01),
            "G2": len(group_02),
        },
    }

@app.get("/tasks/stats_group_grad")
def get_group_grade_stats():
    db = SessionLocal()

    query = db.execute(text("SELECT grad_mean, \"group\" FROM task"))
    rows = query.fetchall()

    db.close()

    group_01 = [row.grad_mean for row in rows if row.group == "G1"]
    group_02 = [row.grad_mean for row in rows if row.group == "G2"]

    return {
        "labels": ["G1", "G2"],
        "boxplot": [
            quartiles(group_01),
            quartiles(group_02),
        ],
        "count": {
            "G1": len(group_01),
            "G2": len(group_02),
        },
    }

@app.get("/tasks/stats_quality_llm")
def get_quality_tasks_stats():
    db = SessionLocal()

    query = db.execute(text("SELECT grad_mean, llm FROM task"))
    rows = query.fetchall()

    db.close()

    quality_llm_true = [row.grad_mean for row in rows if row.llm]
    quality_llm_false = [row.grad_mean for row in rows if not row.llm]

    return {
        "labels": ["With LLM", "Without LLM"],
        "boxplot": [
            quartiles(quality_llm_true),
            quartiles(quality_llm_false),
        ],
        "count": {
            "with_llm": len(quality_llm_true),
            "without_llm": len(quality_llm_false),
        },
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

OLLAMA_URL = "http://ollama:11434/api/generate"
OLLAMA_MODEL = "phi3:mini"

def evaluate_with_llm(task: dict) -> dict:
    prompt = f"""
Você é um avaliador de Engenharia de Software.

Avalie a história de usuário usando APENAS os scores 0, 5 ou 10.

Critérios:
- Score 0: O participante não tentou a tarefa ou falhou em atender aos elementos obrigatórios.
- Score 5: O participante atendeu parcialmente à tarefa. O motivo do score DEVE ser explicado.
- Score 10: O participante atendeu completamente à tarefa. NÃO escreva comentário.

História de usuário (padrão esperado: "Como <persona>, quero <ação>, para <benefício>"):

Descrição:
{task["description"]}

Fluxo principal:
{task["main_flow"]}

Fluxos alternativos:
{task["alt_flow"]}

Formato da resposta (siga exatamente):
Score: <0|5|10>
Comentário: <texto ou vazio>
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False,
            "temperature": 0.0
        },
        timeout=300
    )

    text = response.json()["response"]

    score = None
    comment = ""

    for line in text.splitlines():
        if line.startswith("Score:"):
            score = int(line.replace("Score:", "").strip())
        elif line.startswith("Comentário:"):
            comment = line.replace("Comentário:", "").strip()

    if score != 10 and not comment:
        comment = "Comentário não fornecido pelo avaliador."

    return {
        "score": score,
        "comment": comment
    }


@app.post("/task_evaluate")
def task_evaluate(code: str = Body(..., embed=True)):
    db = SessionLocal()
    try:
        query = db.execute(
            text("""
                SELECT code, description, main_flow, alt_flow
                FROM task
                WHERE code = :code
            """),
            {"code": code}
        )

        row = query.fetchone()
        if not row:
            return {"error": "Task not found"}

        task = dict(row._mapping)

    finally:
        db.close()

    evaluation = evaluate_with_llm(task)

    return {
            "task": task,
            "evaluation": {
                "score": evaluation["score"],
                "comment": evaluation["comment"],
            }
        }

