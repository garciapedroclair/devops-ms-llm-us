from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import checkDB, task, participant, skill

app = FastAPI(title="LLM for US Microservice")

app.add_middleware(
    CORSMiddleware,
    allow_origins= "http://localhost:3001",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(checkDB.router)
app.include_router(task.router)
app.include_router(participant.router)
app.include_router(skill.router)

