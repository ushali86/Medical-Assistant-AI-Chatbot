from fastapi import FastAPI

from .database import Base, engine
from .routes.auth import router as auth_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="MedAssist AI",
    description="AI-assisted Medical Assistant Chatbot",
    version="1.0.0"
)

app.include_router(auth_router)


@app.get("/")
def home():
    return {
        "message": "Welcome to MedAssist AI",
        "status": "API is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }