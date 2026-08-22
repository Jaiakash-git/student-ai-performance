from fastapi import FastAPI
from pydantic import BaseModel

from nlp.assistant import process_message


app = FastAPI(
    title="Student AI Assistant API",
    description="API for Student AI Assistant",
    version="1.0.0"
)


# ==========================================
# REQUEST MODEL
# ==========================================

class ChatRequest(BaseModel):
    student_name: str
    message: str
    context: dict | None = None


# ==========================================
# ROOT
# ==========================================

@app.get("/")
def root():
    return {
        "message": "Student AI Assistant API is running"
    }


# ==========================================
# HEALTH
# ==========================================

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


# ==========================================
# CHAT
# ==========================================

@app.post("/chat")
def chat(request: ChatRequest):

    context = request.context

    response, updated_context = process_message(
        request.student_name,
        request.message,
        context
    )

    return {
        "response": response,
        "context": updated_context
    }