from fastapi import FastAPI, HTTPException

from fastapi.middleware.cors import CORSMiddleware

from api.schemas import ChatRequest, ChatResponse

from agent.agent_core import run_agent


app = FastAPI(
    title="Student AI Assistant API",
    description="API for Student AI Assistant",
    version="1.0.0"
)


# ==========================================
# CORS
# ==========================================

app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        "http://localhost:5173"
    ],

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

        # ==================================
        # RUN AI AGENT
        # ==================================

        result = run_agent(
            student_name=request.student_name,
            user_input=request.message,
            context=request.context
        )


        # ==================================
        # CHECK AGENT RESULT
        # ==================================

        if not result["success"]:

            return ChatResponse(
                response=result["response"],
                context=result["context"]
            )


        # ==================================
        # RETURN AGENT RESPONSE
        # ==================================

        return ChatResponse(
            response=result["response"],
            context=result["context"]
        )


    except Exception as error:

        print(
            f"Chat error: {error}"
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "An internal error occurred "
                "while processing your request."
            )
        )