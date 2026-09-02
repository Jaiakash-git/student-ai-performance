# ==========================================
# STUDENT AI ASSISTANT - MAIN API
# ==========================================

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware

from database import get_connection

from api.auth import (
    get_current_user,
    hash_password,
    verify_password,
    create_access_token
)

from api.schemas import (
    ChatRequest,
    ChatResponse,
    DashboardResponse,
    RegisterRequest,
    LoginRequest,
    ChangePasswordRequest,
    AuthResponse
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


# ==========================================
# FASTAPI APPLICATION
# ==========================================

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
# HEALTH CHECK
# ==========================================

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


# ==========================================
# HELPER
# GET AUTHENTICATED STUDENT NAME
# ==========================================

def get_authenticated_student_name(
    current_user: dict
):

    connection = None
    cursor = None

    try:

        connection = get_connection()

        cursor = connection.cursor(
            dictionary=True
        )

        cursor.execute(
            """
            SELECT
                student_id,
                name
            FROM students
            WHERE student_id = %s
            """,
            (
                current_user["student_id"],
            )
        )

        student = cursor.fetchone()

        if student is None:

            raise HTTPException(
                status_code=404,
                detail="Student not found."
            )

        return student["name"]

    except HTTPException:

        raise

    except Exception as error:

        print(
            f"Student lookup error: {error}"
        )

        raise HTTPException(
            status_code=500,
            detail="Unable to identify authenticated student."
        )

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


# ==========================================
# REGISTER
# ==========================================

@app.post(
    "/auth/register",
    response_model=AuthResponse
)
def register(
    request: RegisterRequest
):

    connection = None
    cursor = None

    try:

        connection = get_connection()

        cursor = connection.cursor(
            dictionary=True
        )

        # --------------------------------------
        # CHECK STUDENT
        # --------------------------------------

        cursor.execute(
            """
            SELECT
                student_id,
                name
            FROM students
            WHERE student_id = %s
            """,
            (
                request.student_id,
            )
        )

        student = cursor.fetchone()

        if student is None:

            raise HTTPException(
                status_code=404,
                detail="Student not found."
            )

        # --------------------------------------
        # CHECK EXISTING USERNAME
        # --------------------------------------

        cursor.execute(
            """
            SELECT
                user_id
            FROM users
            WHERE username = %s
            """,
            (
                request.username,
            )
        )

        existing_user = cursor.fetchone()

        if existing_user is not None:

            raise HTTPException(
                status_code=409,
                detail="Username already exists."
            )

        # --------------------------------------
        # CHECK STUDENT ALREADY REGISTERED
        # --------------------------------------

        cursor.execute(
            """
            SELECT
                user_id
            FROM users
            WHERE student_id = %s
            """,
            (
                request.student_id,
            )
        )

        existing_student = cursor.fetchone()

        if existing_student is not None:

            raise HTTPException(
                status_code=409,
                detail="This student already has an account."
            )

        # --------------------------------------
        # HASH PASSWORD
        # --------------------------------------

        password_hash = hash_password(
            request.password
        )

        # --------------------------------------
        # CREATE USER
        # --------------------------------------

        cursor.execute(
            """
            INSERT INTO users
            (
                student_id,
                username,
                password_hash
            )
            VALUES (%s, %s, %s)
            """,
            (
                request.student_id,
                request.username,
                password_hash
            )
        )

        connection.commit()

        # --------------------------------------
        # RETURN RESPONSE
        # --------------------------------------

        return AuthResponse(
          message="Registration successful.",
          access_token="",
          token_type="bearer",
          student_id=request.student_id,
          username=request.username,
          student_name=student["name"]
        )

    except HTTPException:

        raise

    except Exception as error:

        print(
            f"Registration error: {error}"
        )

        raise HTTPException(
            status_code=500,
            detail="Registration failed."
        )

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


# ==========================================
# LOGIN
# ==========================================

@app.post(
    "/auth/login",
    response_model=AuthResponse
)
def login(
    request: LoginRequest
):

    connection = None
    cursor = None

    try:

        connection = get_connection()

        cursor = connection.cursor(
            dictionary=True
        )

        # --------------------------------------
        # FIND USER
        # --------------------------------------

        cursor.execute(
            """
            SELECT
                user_id,
                student_id,
                username,
                password_hash
            FROM users
            WHERE username = %s
            """,
            (
                request.username,
            )
        )

        user = cursor.fetchone()

        if user is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid username or password."
            )

        # --------------------------------------
        # VERIFY PASSWORD
        # --------------------------------------

        password_valid = verify_password(
            request.password,
            user["password_hash"]
        )

        if not password_valid:
            raise HTTPException(
                status_code=401,
                detail="Invalid username or password."
            )

        # --------------------------------------
        # GET STUDENT NAME
        # --------------------------------------

        cursor.execute(
            """
            SELECT
                name
            FROM students
            WHERE student_id = %s
            """,
            (
                user["student_id"],
            )
        )

        student = cursor.fetchone()

        if student is None:
            raise HTTPException(
                status_code=404,
                detail="Student not found."
            )

        student_name = student["name"]

        # --------------------------------------
        # CREATE JWT TOKEN
        # --------------------------------------

        access_token = create_access_token(
            {
                "user_id": user["user_id"],
                "student_id": user["student_id"],
                "username": user["username"]
            }
        )

        # --------------------------------------
        # RETURN LOGIN RESPONSE
        # --------------------------------------

        return AuthResponse(
            message="Login successful.",
            access_token=access_token,
            token_type="bearer",
            student_id=user["student_id"],
            username=user["username"],
            student_name=student_name
        )

    except HTTPException:
        raise

    except Exception as error:

        print(
            f"Login error: {error}"
        )

        raise HTTPException(
            status_code=500,
            detail="Login failed."
        )

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()

# ==========================================
# CHANGE PASSWORD
# ==========================================

@app.post("/auth/change-password")
def change_password(
    request: ChangePasswordRequest,
    current_user: dict = Depends(
        get_current_user
    )
):

    connection = None
    cursor = None

    try:

        connection = get_connection()

        cursor = connection.cursor(
            dictionary=True
        )

        # --------------------------------------
        # GET CURRENT USER
        # --------------------------------------

        cursor.execute(
            """
            SELECT
                user_id,
                password_hash
            FROM users
            WHERE student_id = %s
            """,
            (
                current_user["student_id"],
            )
        )

        user = cursor.fetchone()

        if user is None:

            raise HTTPException(
                status_code=404,
                detail="User account not found."
            )

        # --------------------------------------
        # VERIFY CURRENT PASSWORD
        # --------------------------------------

        password_valid = verify_password(
            request.current_password,
            user["password_hash"]
        )

        if not password_valid:

            raise HTTPException(
                status_code=401,
                detail="Current password is incorrect."
            )

        # --------------------------------------
        # CHECK SAME PASSWORD
        # --------------------------------------

        if verify_password(
            request.new_password,
            user["password_hash"]
        ):

            raise HTTPException(
                status_code=400,
                detail="New password must be different from the current password."
            )

        # --------------------------------------
        # HASH NEW PASSWORD
        # --------------------------------------

        new_password_hash = hash_password(
            request.new_password
        )

        # --------------------------------------
        # UPDATE PASSWORD
        # --------------------------------------

        cursor.execute(
            """
            UPDATE users
            SET password_hash = %s
            WHERE user_id = %s
            """,
            (
                new_password_hash,
                user["user_id"]
            )
        )

        connection.commit()

        # --------------------------------------
        # SUCCESS
        # --------------------------------------

        return {
            "message": "Password changed successfully."
        }

    except HTTPException:

        raise

    except Exception as error:

        if connection:
            connection.rollback()

        print(
            f"Change password error: {error}"
        )

        raise HTTPException(
            status_code=500,
            detail="Unable to change password."
        )

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()
            
# ==========================================
# DASHBOARD
# ==========================================

@app.get(
    "/student/{student_name}/dashboard",
    response_model=DashboardResponse
)
def dashboard(
    student_name: str,
    current_user: dict = Depends(
        get_current_user
    )
):

    try:

        # ======================================
        # GET AUTHENTICATED STUDENT
        # ======================================

        authenticated_student_name = (
            get_authenticated_student_name(
                current_user
            )
        )

        # ======================================
        # SECURITY CHECK
        # ======================================

        if (
            student_name.lower()
            != authenticated_student_name.lower()
        ):

            raise HTTPException(
                status_code=403,
                detail="You are not authorized to access this student's data."
            )

        # ======================================
        # GET STUDENT DATA
        # ======================================

        average_result = get_average(
            authenticated_student_name
        )

        attendance_result = get_attendance(
            authenticated_student_name
        )

        performance_result = get_performance(
            authenticated_student_name
        )

        risk_result = get_risk(
            authenticated_student_name
        )

        highest_result = get_highest_subject(
            authenticated_student_name
        )

        lowest_result = get_lowest_subject(
            authenticated_student_name
        )

        trend_result = get_trend(
            authenticated_student_name
        )

        recommendation_result = get_recommendation(
            authenticated_student_name
        )

        # ======================================
        # CHECK RESULTS
        # ======================================

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

            if not result.get(
                "success",
                False
            ):

                raise HTTPException(
                    status_code=404,
                    detail=result.get(
                        "message",
                        "Student data not found."
                    )
                )

        # ======================================
        # RETURN DASHBOARD
        # ======================================

        return DashboardResponse(

            student_name=authenticated_student_name,

            average=average_result[
                "average"
            ],

            attendance=attendance_result[
                "attendance"
            ],

            performance_status=performance_result[
                "status"
            ],

            risk_level=risk_result[
                "risk_level"
            ],

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
def chat(
    request: ChatRequest,
    current_user: dict = Depends(
        get_current_user
    )
):

    try:

        authenticated_student_name = (
            get_authenticated_student_name(
                current_user
            )
        )

        result = run_agent(
            student_name=authenticated_student_name,
            user_input=request.message,
            context=request.context
        )

        if not result["success"]:

            return ChatResponse(
                response=result["response"],
                context=result["context"]
            )

        return ChatResponse(
            response=result["response"],
            context=result["context"]
        )

    except HTTPException:
        raise

    except Exception as error:

        print(f"Chat error: {error}")

        raise HTTPException(
            status_code=500,
            detail=(
                "An internal error occurred "
                "while processing your request."
            )
        )