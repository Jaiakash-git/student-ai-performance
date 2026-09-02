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
    create_access_token,

    # Password reset
    generate_reset_code,
    hash_reset_code,
    verify_reset_code,
    RESET_CODE_EXPIRE_MINUTES,

    # Email verification
    generate_email_verification_code,
    hash_email_verification_code,
    verify_email_verification_code,
    EMAIL_VERIFICATION_EXPIRE_MINUTES
)

from api.schemas import (
    ChatRequest,
    ChatResponse,
    DashboardResponse,
    RegisterRequest,
    LoginRequest,
    ChangePasswordRequest,
    AuthResponse,

    # Email verification
    SendEmailVerificationRequest,
    VerifyEmailRequest,

    # Password reset
    ForgotPasswordRequest,
    VerifyResetCodeRequest,
    ResetPasswordRequest
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

from datetime import datetime, timedelta
import hmac
import os
import smtplib
from email.message import EmailMessage


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
            detail=(
                "Unable to identify "
                "authenticated student."
            )
        )

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()


# ==========================================
# EMAIL CONFIGURATION
# ==========================================

SMTP_HOST = os.getenv(
    "SMTP_HOST",
    ""
)

SMTP_PORT = int(
    os.getenv(
        "SMTP_PORT",
        "587"
    )
)

SMTP_USERNAME = os.getenv(
    "SMTP_USERNAME",
    ""
)

SMTP_PASSWORD = os.getenv(
    "SMTP_PASSWORD",
    ""
)

SMTP_FROM_EMAIL = os.getenv(
    "SMTP_FROM_EMAIL",
    SMTP_USERNAME
)


# ==========================================
# SEND PASSWORD RESET EMAIL
# ==========================================

def send_reset_code_email(
    recipient_email: str,
    reset_code: str
):

    if not all(
        [
            SMTP_HOST,
            SMTP_USERNAME,
            SMTP_PASSWORD,
            SMTP_FROM_EMAIL
        ]
    ):
        raise RuntimeError(
            "SMTP email configuration is incomplete."
        )

    message = EmailMessage()

    message["Subject"] = (
        "Student AI Assistant - Password Reset"
    )

    message["From"] = SMTP_FROM_EMAIL
    message["To"] = recipient_email

    message.set_content(
        f"""
Hello,

A password reset request was made for your
Student AI Assistant account.

Your verification code is:

{reset_code}

This code expires in
{RESET_CODE_EXPIRE_MINUTES} minutes.

If you did not request a password reset,
you can safely ignore this email.

Student AI Assistant
"""
    )

    with smtplib.SMTP(
        SMTP_HOST,
        SMTP_PORT,
        timeout=15
    ) as server:

        server.starttls()

        server.login(
            SMTP_USERNAME,
            SMTP_PASSWORD
        )

        server.send_message(
            message
        )


# ==========================================
# SEND EMAIL VERIFICATION CODE
# ==========================================

def send_email_verification_code(
    recipient_email: str,
    verification_code: str
):

    if not all(
        [
            SMTP_HOST,
            SMTP_USERNAME,
            SMTP_PASSWORD,
            SMTP_FROM_EMAIL
        ]
    ):
        raise RuntimeError(
            "SMTP email configuration is incomplete."
        )

    message = EmailMessage()

    message["Subject"] = (
        "Student AI Assistant - Email Verification"
    )

    message["From"] = SMTP_FROM_EMAIL
    message["To"] = recipient_email

    message.set_content(
        f"""
Hello,

A request was made to verify this email address
for your Student AI Assistant account.

Your verification code is:

{verification_code}

This code expires in
{EMAIL_VERIFICATION_EXPIRE_MINUTES} minutes.

If you did not request this verification,
you can safely ignore this email.

Student AI Assistant
"""
    )

    with smtplib.SMTP(
        SMTP_HOST,
        SMTP_PORT,
        timeout=15
    ) as server:

        server.starttls()

        server.login(
            SMTP_USERNAME,
            SMTP_PASSWORD
        )

        server.send_message(
            message
        )


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
                detail=(
                    "This student already "
                    "has an account."
                )
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

        if connection:
            connection.rollback()

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
                detail=(
                    "Invalid username "
                    "or password."
                )
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
                detail=(
                    "Invalid username "
                    "or password."
                )
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
                detail=(
                    "Current password is incorrect."
                )
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
                detail=(
                    "New password must be different "
                    "from the current password."
                )
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
            "message": (
                "Password changed successfully."
            )
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
            detail=(
                "Unable to change password."
            )
        )

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


# ==========================================
# SEND EMAIL VERIFICATION
# ==========================================

@app.post("/auth/send-email-verification")
def send_email_verification(
    request: SendEmailVerificationRequest
):

    connection = None
    cursor = None

    generic_response = {
        "message": (
            "If the account details are valid, "
            "a verification code has been sent."
        )
    }

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
                username,
                email,
                email_verified
            FROM users
            WHERE username = %s
            """,
            (
                request.username,
            )
        )

        user = cursor.fetchone()

        # --------------------------------------
        # GENERIC RESPONSE
        # --------------------------------------

        if user is None:
            return generic_response

        # --------------------------------------
        # EMAIL MUST EXIST
        # --------------------------------------

        if not user["email"]:

            # For the initial setup, we allow
            # the supplied email to be registered
            # with the existing account.
            #
            # The email will NOT be considered
            # verified until the code is confirmed.

            supplied_email = (
                request.email.strip().lower()
            )

            cursor.execute(
                """
                UPDATE users
                SET
                    email = %s,
                    email_verified = FALSE
                WHERE user_id = %s
                """,
                (
                    supplied_email,
                    user["user_id"]
                )
            )

            connection.commit()

            stored_email = supplied_email

        else:

            # ----------------------------------
            # EXISTING EMAIL
            # ----------------------------------

            stored_email = (
                user["email"]
                .strip()
                .lower()
            )

            supplied_email = (
                request.email
                .strip()
                .lower()
            )

            if not hmac.compare_digest(
                stored_email,
                supplied_email
            ):
                return generic_response

        # --------------------------------------
        # ALREADY VERIFIED
        # --------------------------------------

        if user["email_verified"]:

            return {
                "message": "Email is already verified."
            }

        # --------------------------------------
        # GENERATE VERIFICATION CODE
        # --------------------------------------

        verification_code = (
            generate_email_verification_code()
        )

        # --------------------------------------
        # HASH CODE
        # --------------------------------------

        code_hash = (
            hash_email_verification_code(
                verification_code
            )
        )

        # --------------------------------------
        # CREATE EXPIRATION
        # --------------------------------------

        expires_at = (
            datetime.utcnow()
            + timedelta(
                minutes=EMAIL_VERIFICATION_EXPIRE_MINUTES
            )
        )

        # --------------------------------------
        # STORE VERIFICATION DATA
        # --------------------------------------

        cursor.execute(
            """
            UPDATE users
            SET
                email_verification_code_hash = %s,
                email_verification_expires_at = %s,
                email_verification_used = FALSE
            WHERE user_id = %s
            """,
            (
                code_hash,
                expires_at,
                user["user_id"]
            )
        )

        connection.commit()

        # --------------------------------------
        # SEND EMAIL
        # --------------------------------------

        try:

            send_email_verification_code(
                stored_email,
                verification_code
            )

        except Exception as email_error:

            # Invalidate verification code
            cursor.execute(
                """
                UPDATE users
                SET
                    email_verification_code_hash = NULL,
                    email_verification_expires_at = NULL,
                    email_verification_used = FALSE
                WHERE user_id = %s
                """,
                (
                    user["user_id"],
                )
            )

            connection.commit()

            print(
                "Email verification error: "
                f"{email_error}"
            )

            raise HTTPException(
                status_code=500,
                detail=(
                    "Unable to send verification email."
                )
            )

        return generic_response

    except HTTPException:
        raise

    except Exception as error:

        if connection:
            connection.rollback()

        print(
            f"Send email verification error: {error}"
        )

        return generic_response

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


# ==========================================
# VERIFY EMAIL
# ==========================================

@app.post("/auth/verify-email")
def verify_email(
    request: VerifyEmailRequest
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
                email_verified,
                email_verification_code_hash,
                email_verification_expires_at,
                email_verification_used
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
                status_code=400,
                detail="Invalid verification request."
            )

        # --------------------------------------
        # ALREADY VERIFIED
        # --------------------------------------

        if user["email_verified"]:

            return {
                "message": "Email is already verified."
            }

        # --------------------------------------
        # CHECK CODE
        # --------------------------------------

        code_hash = (
            user[
                "email_verification_code_hash"
            ]
        )

        expires_at = (
            user[
                "email_verification_expires_at"
            ]
        )

        if not code_hash or not expires_at:

            raise HTTPException(
                status_code=400,
                detail=(
                    "No active verification code."
                )
            )

        # --------------------------------------
        # CHECK USED
        # --------------------------------------

        if user["email_verification_used"]:

            raise HTTPException(
                status_code=400,
                detail=(
                    "Verification code has "
                    "already been used."
                )
            )

        # --------------------------------------
        # CHECK EXPIRATION
        # --------------------------------------

        if datetime.utcnow() > expires_at:

            raise HTTPException(
                status_code=400,
                detail=(
                    "Verification code has expired."
                )
            )

        # --------------------------------------
        # VERIFY CODE
        # --------------------------------------

        if not verify_email_verification_code(
            request.verification_code,
            code_hash
        ):

            raise HTTPException(
                status_code=400,
                detail="Invalid verification code."
            )

        # --------------------------------------
        # MARK EMAIL AS VERIFIED
        # --------------------------------------

        cursor.execute(
            """
            UPDATE users
            SET
                email_verified = TRUE,
                email_verification_code_hash = NULL,
                email_verification_expires_at = NULL,
                email_verification_used = TRUE
            WHERE user_id = %s
            """,
            (
                user["user_id"],
            )
        )

        connection.commit()

        # --------------------------------------
        # SUCCESS
        # --------------------------------------

        return {
            "message": (
                "Email verified successfully."
            )
        }

    except HTTPException:
        raise

    except Exception as error:

        if connection:
            connection.rollback()

        print(
            f"Verify email error: {error}"
        )

        raise HTTPException(
            status_code=500,
            detail="Unable to verify email."
        )

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


# ==========================================
# FORGOT PASSWORD
# ==========================================

@app.post("/auth/forgot-password")
def forgot_password(
    request: ForgotPasswordRequest
):

    connection = None
    cursor = None

    generic_response = {
        "message": (
            "If the account details are valid, "
            "a verification code has been sent."
        )
    }

    try:
        connection = get_connection()

        cursor = connection.cursor(
            dictionary=True
        )

        # --------------------------------------
        # FIND ACCOUNT
        # --------------------------------------

        cursor.execute(
            """
            SELECT
                user_id,
                username,
                email,
                email_verified
            FROM users
            WHERE username = %s
            """,
            (
                request.username,
            )
        )

        user = cursor.fetchone()

        # --------------------------------------
        # DO NOT REVEAL ACCOUNT EXISTENCE
        # --------------------------------------

        if user is None:
            return generic_response

        # --------------------------------------
        # CHECK EMAIL
        # --------------------------------------

        if not user["email"]:
            return generic_response

        # --------------------------------------
        # CHECK EMAIL VERIFICATION
        # --------------------------------------

        if not user["email_verified"]:
            return generic_response

        # --------------------------------------
        # SECURE EMAIL COMPARISON
        # --------------------------------------

        stored_email = (
            user["email"]
            .strip()
            .lower()
        )

        supplied_email = (
            request.email
            .strip()
            .lower()
        )

        if not hmac.compare_digest(
            stored_email,
            supplied_email
        ):
            return generic_response

        # --------------------------------------
        # GENERATE SECURE RESET CODE
        # --------------------------------------

        reset_code = generate_reset_code()

        # --------------------------------------
        # HASH CODE
        # --------------------------------------

        reset_code_hash = (
            hash_reset_code(
                reset_code
            )
        )

        # --------------------------------------
        # CREATE EXPIRATION
        # --------------------------------------

        expires_at = (
            datetime.utcnow()
            + timedelta(
                minutes=RESET_CODE_EXPIRE_MINUTES
            )
        )

        # --------------------------------------
        # STORE RESET INFORMATION
        # --------------------------------------

        cursor.execute(
            """
            UPDATE users
            SET
                reset_token_hash = %s,
                reset_token_expires_at = %s,
                reset_token_used = FALSE
            WHERE user_id = %s
            """,
            (
                reset_code_hash,
                expires_at,
                user["user_id"]
            )
        )

        connection.commit()

        # --------------------------------------
        # SEND EMAIL
        # --------------------------------------

        try:

            send_reset_code_email(
                stored_email,
                reset_code
            )

        except Exception as email_error:

            # Invalidate reset code
            cursor.execute(
                """
                UPDATE users
                SET
                    reset_token_hash = NULL,
                    reset_token_expires_at = NULL,
                    reset_token_used = FALSE
                WHERE user_id = %s
                """,
                (
                    user["user_id"],
                )
            )

            connection.commit()

            print(
                "Password reset email error: "
                f"{email_error}"
            )

        return generic_response

    except Exception as error:

        if connection:
            connection.rollback()

        print(
            f"Forgot password error: {error}"
        )

        return generic_response

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


# ==========================================
# VERIFY RESET CODE
# ==========================================

@app.post("/auth/verify-reset-code")
def verify_reset_code_endpoint(
    request: VerifyResetCodeRequest
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
                reset_token_hash,
                reset_token_expires_at,
                reset_token_used
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
                status_code=400,
                detail=(
                    "Invalid or expired "
                    "verification code."
                )
            )

        # --------------------------------------
        # CHECK CODE EXISTS
        # --------------------------------------

        if user["reset_token_hash"] is None:

            raise HTTPException(
                status_code=400,
                detail=(
                    "Invalid or expired "
                    "verification code."
                )
            )

        # --------------------------------------
        # CHECK USED
        # --------------------------------------

        if user["reset_token_used"]:

            raise HTTPException(
                status_code=400,
                detail=(
                    "Invalid or expired "
                    "verification code."
                )
            )

        # --------------------------------------
        # CHECK EXPIRATION
        # --------------------------------------

        if (
            user["reset_token_expires_at"] is None
            or datetime.utcnow()
            > user["reset_token_expires_at"]
        ):

            raise HTTPException(
                status_code=400,
                detail=(
                    "Invalid or expired "
                    "verification code."
                )
            )

        # --------------------------------------
        # VERIFY CODE
        # --------------------------------------

        if not verify_reset_code(
            request.verification_code,
            user["reset_token_hash"]
        ):

            raise HTTPException(
                status_code=400,
                detail=(
                    "Invalid or expired "
                    "verification code."
                )
            )

        # --------------------------------------
        # SUCCESS
        # --------------------------------------

        return {
            "message": (
                "Verification code is valid."
            )
        }

    except HTTPException:
        raise

    except Exception as error:

        print(
            f"Verify reset code error: {error}"
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "Unable to verify the code."
            )
        )

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


# ==========================================
# RESET PASSWORD
# ==========================================

@app.post("/auth/reset-password")
def reset_password(
    request: ResetPasswordRequest
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
                password_hash,
                reset_token_hash,
                reset_token_expires_at,
                reset_token_used
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
                status_code=400,
                detail=(
                    "Invalid or expired "
                    "verification code."
                )
            )

        # --------------------------------------
        # CHECK RESET CODE
        # --------------------------------------

        if user["reset_token_hash"] is None:

            raise HTTPException(
                status_code=400,
                detail=(
                    "Invalid or expired "
                    "verification code."
                )
            )

        if user["reset_token_used"]:

            raise HTTPException(
                status_code=400,
                detail=(
                    "Invalid or expired "
                    "verification code."
                )
            )

        # --------------------------------------
        # CHECK EXPIRATION
        # --------------------------------------

        if (
            user["reset_token_expires_at"] is None
            or datetime.utcnow()
            > user["reset_token_expires_at"]
        ):

            raise HTTPException(
                status_code=400,
                detail=(
                    "Invalid or expired "
                    "verification code."
                )
            )

        # --------------------------------------
        # VERIFY RESET CODE
        # --------------------------------------

        if not verify_reset_code(
            request.verification_code,
            user["reset_token_hash"]
        ):

            raise HTTPException(
                status_code=400,
                detail=(
                    "Invalid or expired "
                    "verification code."
                )
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
                detail=(
                    "New password must be different "
                    "from the previous password."
                )
            )

        # --------------------------------------
        # HASH NEW PASSWORD
        # --------------------------------------

        new_password_hash = hash_password(
            request.new_password
        )

        # --------------------------------------
        # UPDATE PASSWORD
        # INVALIDATE RESET CODE
        # --------------------------------------

        cursor.execute(
            """
            UPDATE users
            SET
                password_hash = %s,
                reset_token_hash = NULL,
                reset_token_expires_at = NULL,
                reset_token_used = TRUE
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
            "message": (
                "Password reset successfully."
            )
        }

    except HTTPException:
        raise

    except Exception as error:

        if connection:
            connection.rollback()

        print(
            f"Reset password error: {error}"
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "Unable to reset password."
            )
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
                detail=(
                    "You are not authorized to "
                    "access this student's data."
                )
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

        recommendation_result = (
            get_recommendation(
                authenticated_student_name
            )
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

            student_name=(
                authenticated_student_name
            ),

            average=average_result[
                "average"
            ],

            attendance=attendance_result[
                "attendance"
            ],

            performance_status=(
                performance_result[
                    "status"
                ]
            ),

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

            average_improvement=(
                trend_result[
                    "average_improvement"
                ]
            ),

            recommendation=(
                recommendation_result[
                    "recommendation"
                ]
            ),

            priority_subject=(
                recommendation_result[
                    "priority_subject"
                ]
            ),

            priority_mark=(
                recommendation_result[
                    "priority_mark"
                ]
            )
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
            student_name=(
                authenticated_student_name
            ),
            user_input=request.message,
            context=request.context
        )

        return ChatResponse(
            response=result["response"],
            context=result["context"]
        )

    except HTTPException:
        raise

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

