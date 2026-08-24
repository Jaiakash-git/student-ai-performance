from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from api.schemas import ChatRequest, ChatResponse
from nlp.assistant import process_message


app = FastAPI(
    title="Student AI Assistant API",
    description="API for Student AI Assistant",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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

@app.post(
    "/chat",
    response_model=ChatResponse
)
def chat(request: ChatRequest):

    try:
        response, updated_context = process_message(
            request.student_name,
            request.message,
            request.context
        )

        return ChatResponse(
            response=response,
            context=updated_context
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="An internal error occurred while processing your request."
        )