from fastapi import FastAPI
from app.routers import checkDB, task, participant, skill

app = FastAPI(title="LLM for US Microservice")

app.include_router(checkDB.router)
app.include_router(task.router)
app.include_router(participant.router)
app.include_router(skill.router)