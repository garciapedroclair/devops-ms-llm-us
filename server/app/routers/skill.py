from fastapi import APIRouter, Query
from sqlalchemy import text
from ..utils.db import SessionLocal
import numpy as np

router = APIRouter()

@router.get("/skill/time")
def time_by_skill(skill: str = Query(..., description="Skill to filter (e.g., agile_methods)")):
    numeric_skills = ["sw_project_mgmt", "requirements", "agile_methods", "participantage"]
    if skill not in numeric_skills:
        return {"error": f"Skill '{skill}' is not valid. Choose one of {numeric_skills}"}

    db = SessionLocal()
    try:
        query = db.execute(text(f"""
            SELECT 
                p.{skill} AS skill_level,
                t.time
            FROM participant p
            JOIN task t
                ON p.code = t.code
            WHERE t.time IS NOT NULL
        """))
        rows = query.fetchall()
        columns = query.keys()

        # Monta lista de dicionários
        data = [dict(zip(columns, row)) for row in rows]

        # Agrupa por nível de conhecimento
        grouped = {
            "low": [d["time"] for d in data if d["skill_level"] in (1, 2)],
            "medium": [d["time"] for d in data if d["skill_level"] == 3],
            "high": [d["time"] for d in data if d["skill_level"] in (4, 5)]
        }

        return grouped
    finally:
        db.close()


@router.get("/skill/grade")
def grade_by_skill(skill: str = Query(..., description="Skill to filter (e.g., agile_methods)")):
    numeric_skills = ["sw_project_mgmt", "requirements", "agile_methods", "participantage"]
    if skill not in numeric_skills:
        return {"error": f"Skill '{skill}' is not valid. Choose one of {numeric_skills}"}

    db = SessionLocal()
    try:
        query = db.execute(text(f"""
            SELECT 
                p.{skill} AS skill_level,
                t.grad_mean
            FROM participant p
            JOIN task t
                ON p.code = t.code
            WHERE t.llm = true
              AND t.grad_mean IS NOT NULL
        """))
        rows = query.fetchall()
        columns = query.keys()

        # Monta lista de dicionários
        data = [dict(zip(columns, row)) for row in rows]

        # Agrupa por nível de conhecimento
        grouped = {
            "low": [d["grad_mean"] for d in data if d["skill_level"] in (1, 2)],
            "medium": [d["grad_mean"] for d in data if d["skill_level"] == 3],
            "high": [d["grad_mean"] for d in data if d["skill_level"] in (4, 5)]
        }

        return grouped
    finally:
        db.close()

@router.get("/skill/aggregate")
def skill_aggregate(
    skill: str = Query(..., description="Skill column name"),
    metric: str = Query("time", description="time or grade")  # aqui pode ser "time" ou "grad_mean"
):
    db = SessionLocal()
    try:
        # Valida metric
        if metric not in ("time", "grad_mean"):
            return {"error": "metric must be 'time' or 'grad_mean'"}

        query = db.execute(text(f"""
            SELECT 
                p.{skill} as skill_level,
                t.{metric} as metric_value
            FROM participant p
            JOIN task t
              ON p.code = t.code
            WHERE t.llm = TRUE
              AND t.{metric} IS NOT NULL
        """))
        rows = query.fetchall()

        groups = {"low": [], "medium": [], "high": []}
        for row in rows:
            level = row.skill_level
            value = row.metric_value
            if level in (1, 2):
                groups["low"].append(value)
            elif level == 3:
                groups["medium"].append(value)
            elif level in (4, 5):
                groups["high"].append(value)

        # Calcular média e desvio padrão
        result = {}
        for k, v in groups.items():
            arr = np.array(v)
            if len(arr) > 0:
                result[k] = {"mean": float(arr.mean()), "std": float(arr.std())}
            else:
                result[k] = {"mean": 0, "std": 0}

        return result
    finally:
        db.close()


