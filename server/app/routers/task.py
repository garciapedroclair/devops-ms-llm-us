from fastapi import APIRouter, Body
from sqlalchemy import text
from ..utils.db import SessionLocal
from ..utils.statistic import quartiles
from ..utils.prompt import evaluate_with_llm

router = APIRouter()

@router.post("/task_evaluate")
def task_evaluate(code: str = Body(..., embed=True), task_id: str = Body(..., embed=True)):
    db = SessionLocal()
    try:
        query = db.execute(
            text("""
                SELECT code, task_id, description, main_flow, alt_flow
                FROM task
                WHERE code = :code AND task_id = :task_id
            """),
            {"code": code, "task_id": task_id}
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



@router.get("/tasks/stats_time_llm")
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

@router.get("/tasks/stats_group_time")
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

@router.get("/tasks/stats_group_grad")
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

@router.get("/tasks/stats_quality_llm")
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
