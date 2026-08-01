from fastapi import FastAPI, Depends
from dotenv import load_dotenv

load_dotenv()
from fastapi.middleware.cors import CORSMiddleware

from . import models
from .database import Base, engine

from .routes.auth import (
    router as auth_router,
    get_current_user
)

from .routes.chat import (
    router as chat_router
)


# ===========================
# DATABASE INITIALIZATION
# ===========================

Base.metadata.create_all(
    bind=engine
)


# ===========================
# FASTAPI APP
# ===========================

app = FastAPI(
    title="Medical Assistant AI Chatbot",
    version="1.0.0"
)


# ===========================
# CORS CONFIGURATION
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

app.include_router(
    auth_router
)

app.include_router(
    chat_router
)



# ===========================
# HOME API
# ===========================

@app.get("/")
def home():

    return {
        "message": "Medical Assistant AI Backend Running"
    }



# ===========================
# PROFILE API (JWT TEST)
# ===========================

@app.get("/profile")
def profile(
    user = Depends(get_current_user)
):

    return {
        "message": "Profile Access Successful",
        "user": user
    }