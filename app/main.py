from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Load .env
load_dotenv()

# Import database & models
from .database import Base, engine
from . import models

# Import routers
from .routes.auth import (
    router as auth_router,
    get_current_user
)

from .routes.chat import (
    router as chat_router
)

from .routes.doctor import (
    router as doctor_router
)

# ===========================
# CREATE DATABASE TABLES
# ===========================

Base.metadata.create_all(bind=engine)

# ===========================
# FASTAPI APP
# ===========================

app = FastAPI(
    title="Medical Assistant AI Chatbot",
    description="AI Powered Medical Assistant Backend",
    version="2.0.0"
)

# ===========================
# CORS
# ===========================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===========================
# ROUTERS
# ===========================

app.include_router(auth_router)
app.include_router(chat_router)
app.include_router(doctor_router)

# ===========================
# HOME
# ===========================

@app.get("/")
def home():
    return {
        "success": True,
        "message": "Medical Assistant AI Backend Running 🚀",
        "version": "2.0.0"
    }

# ===========================
# USER PROFILE
# ===========================

@app.get("/profile")
def profile(
    current_user=Depends(get_current_user)
):
    return {
        "success": True,
        "user": current_user
    }

# ===========================
# HEALTH CHECK
# ===========================

@app.get("/health")
def health():
    return {
        "status": "Healthy",
        "database": "Connected",
        "api": "Running"
    }