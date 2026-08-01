from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse

from .database import Base, engine
from .routes.auth import router as auth_router

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="MedAssist AI",
    description="AI Medical Assistant Chatbot",
    version="1.0.0"
)

# Authentication Routes
app.include_router(auth_router)

# Frontend folder
BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"


# ---------------- HOME ----------------

@app.get("/")
def home():
    return FileResponse(FRONTEND_DIR / "index.html")


# ---------------- INDEX ----------------

@app.get("/index.html")
def index():
    return FileResponse(FRONTEND_DIR / "index.html")


# ---------------- LOGIN ----------------

@app.get("/login.html")
def login():
    return FileResponse(FRONTEND_DIR / "login.html")


# ---------------- REGISTER ----------------

@app.get("/register.html")
def register():
    return FileResponse(FRONTEND_DIR / "register.html")


# ---------------- DASHBOARD ----------------

@app.get("/dashboard.html")
def dashboard():
    return FileResponse(FRONTEND_DIR / "dashboard.html")


# ---------------- CHAT ----------------

@app.get("/chat.html")
def chat():
    return FileResponse(FRONTEND_DIR / "chat.html")


# ---------------- CSS ----------------

@app.get("/style.css")
def style():
    return FileResponse(FRONTEND_DIR / "style.css")


# ---------------- HEALTH ----------------

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }