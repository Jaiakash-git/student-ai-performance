from pydantic import BaseModel, Field
from typing import Optional


# =========================================================
# CHAT
# =========================================================

class ChatRequest(BaseModel):
    model_config = {"str_strip_whitespace": True}

    message: str = Field(min_length=1)
    context: Optional[dict] = None


class ChatResponse(BaseModel):
    response: str
    context: dict


# =========================================================
# DASHBOARD
# =========================================================

class DashboardResponse(BaseModel):
    student_name: str

    average: float
    attendance: float

    performance_status: str
    risk_level: str
    risk_probability: float

    highest_subject: str
    highest_mark: float

    lowest_subject: str
    lowest_mark: float

    overall_trend: str
    average_improvement: float

    recommendation: str

    priority_subject: str
    priority_mark: float


# =========================================================
# AUTHENTICATION
# =========================================================

class RegisterRequest(BaseModel):
    model_config = {"str_strip_whitespace": True}

    student_id: int = Field(gt=0)
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=6, max_length=100)


class LoginRequest(BaseModel):
    model_config = {"str_strip_whitespace": True}

    username: str = Field(min_length=1, max_length=50)
    password: str = Field(min_length=1, max_length=100)


class ChangePasswordRequest(BaseModel):
    model_config = {"str_strip_whitespace": True}

    current_password: str = Field(min_length=1, max_length=100)
    new_password: str = Field(min_length=6, max_length=100)


# =========================================================
# EMAIL VERIFICATION
# =========================================================

class SendEmailVerificationRequest(BaseModel):
    model_config = {"str_strip_whitespace": True}

    username: str = Field(min_length=1, max_length=50)
    email: str = Field(min_length=5, max_length=255)


class VerifyEmailRequest(BaseModel):
    model_config = {"str_strip_whitespace": True}

    username: str = Field(min_length=1, max_length=50)
    verification_code: str = Field(min_length=6, max_length=6)


# =========================================================
# FORGOT PASSWORD
# =========================================================

class ForgotPasswordRequest(BaseModel):
    model_config = {"str_strip_whitespace": True}

    username: str = Field(min_length=1, max_length=50)
    email: str = Field(min_length=5, max_length=255)


class VerifyResetCodeRequest(BaseModel):
    model_config = {"str_strip_whitespace": True}

    username: str = Field(min_length=1, max_length=50)
    verification_code: str = Field(min_length=6, max_length=6)


class ResetPasswordRequest(BaseModel):
    model_config = {"str_strip_whitespace": True}

    username: str = Field(min_length=1, max_length=50)
    verification_code: str = Field(min_length=6, max_length=6)
    new_password: str = Field(min_length=6, max_length=100)


# =========================================================
# AUTH RESPONSE
# =========================================================

class AuthResponse(BaseModel):
    message: str
    access_token: str
    token_type: str = "bearer"
    student_id: int
    username: str
    student_name: str

