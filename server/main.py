from fastapi import FastAPI
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(title="Message Microservice")

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "database_url_loaded": bool(os.getenv("DATABASE_URL"))
    }
