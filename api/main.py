from fastapi import FastAPI, HTTPException

from fastapi.middleware.cors import CORSMiddleware

from api.schemas import (
    ChatRequest,
    ChatResponse,
    DashboardResponse
)

from agent.agent_core import run_agent

from agent.tools import (
    get_average,
    get_attendance,
    get_performance,
    get_risk,
    get_highest_subject,
    get_lowest_subject,
    get_trend,
    get_recommendation
)


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
# DASHBOARD
# ==========================================

@app.get(
    "/student/{student_name}/dashboard",
    response_model=DashboardResponse
)
def dashboard(student_name: str):

    try:

        # ==================================
        # GET STUDENT DATA
        # ==================================

        average_result = get_average(
            student_name
        )

        attendance_result = get_attendance(
            student_name
        )

        performance_result = get_performance(
            student_name
        )

        risk_result = get_risk(
            student_name
        )

        highest_result = get_highest_subject(
            student_name
        )

        lowest_result = get_lowest_subject(
            student_name
        )

        trend_result = get_trend(
            student_name
        )

        recommendation_result = get_recommendation(
            student_name
        )


        # ==================================
        # CHECK RESULTS
        # ==================================

        results = [
            average_result,
            attendance_result,
            performance_result,
            risk_result,
            highest_result,
            lowest_result,
            trend_result,
            recommendation_result
        ]

        for result in results:

            if not result.get("success", False):

                raise HTTPException(
                    status_code=404,
                    detail=result.get(
                        "message",
                        "Student data not found."
                    )
                )


        # ==================================
        # RETURN DASHBOARD
        # ==================================

        return DashboardResponse(

            student_name=student_name,

            average=average_result["average"],

            attendance=attendance_result["attendance"],

            performance_status=performance_result["status"],

            risk_level=risk_result["risk_level"],

            risk_probability=risk_result[
                "risk_probability"
            ],

            highest_subject=highest_result[
                "subject"
            ],

            highest_mark=highest_result[
                "mark"
            ],

            lowest_subject=lowest_result[
                "subject"
            ],

            lowest_mark=lowest_result[
                "mark"
            ],

            overall_trend=trend_result[
                "overall_trend"
            ],

            average_improvement=trend_result[
                "average_improvement"
            ],

            recommendation=recommendation_result[
                "recommendation"
            ],

            priority_subject=recommendation_result[
                "priority_subject"
            ],

            priority_mark=recommendation_result[
                "priority_mark"
            ]
        )


    except HTTPException:

        raise


    except Exception as error:

        print(
            f"Dashboard error: {error}"
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "An internal error occurred "
                "while loading the dashboard."
            )
        )


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

