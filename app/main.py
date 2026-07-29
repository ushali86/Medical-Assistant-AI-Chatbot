from fastapi import FastAPI

app = FastAPI(
    title="MedAssist AI",
    description="AI-assisted Medical Assistant Chatbot",
    version="1.0.0"
)


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