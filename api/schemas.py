from pydantic import BaseModel, Field
from typing import Optional


# ==========================================
# CHAT REQUEST
# ==========================================

class ChatRequest(BaseModel):

    model_config = {
        "str_strip_whitespace": True
    }# ==========================================
# STUDENT AI ASSISTANT - API SCHEMAS
# ==========================================

from pydantic import BaseModel, Field
from typing import Optional


# ==========================================
# CHAT REQUEST
# ==========================================

class ChatRequest(BaseModel):

    model_config = {
        "str_strip_whitespace": True
    }

    message: str = Field(
        min_length=1
    )

    context: Optional[dict] = None


# ==========================================
# CHAT RESPONSE
# ==========================================

class ChatResponse(BaseModel):

    response: str

    context: dict


# ==========================================
# DASHBOARD RESPONSE
# ==========================================

class DashboardResponse(BaseModel):

    student_name: str

    # ------------------------------
    # ACADEMIC
    # ------------------------------

    average: float

    attendance: float

    performance_status: str

    # ------------------------------
    # RISK
    # ------------------------------

    risk_level: str

    risk_probability: float

    # ------------------------------
    # SUBJECT PERFORMANCE
    # ------------------------------

    highest_subject: str

    highest_mark: float

    lowest_subject: str

    lowest_mark: float

    # ------------------------------
    # TREND
    # ------------------------------

    overall_trend: str

    average_improvement: float

    # ------------------------------
    # RECOMMENDATION
    # ------------------------------

    recommendation: str

    priority_subject: str

    priority_mark: float


# ==========================================
# REGISTER REQUEST
# ==========================================

class RegisterRequest(BaseModel):

    model_config = {
        "str_strip_whitespace": True
    }

    student_id: int = Field(
        gt=0
    )

    username: str = Field(
        min_length=3,
        max_length=50
    )

    password: str = Field(
        min_length=6,
        max_length=100
    )


# ==========================================
# LOGIN REQUEST
# ==========================================

class LoginRequest(BaseModel):

    model_config = {
        "str_strip_whitespace": True
    }

    username: str = Field(
        min_length=1,
        max_length=50
    )

    password: str = Field(
        min_length=1,
        max_length=100
    )


# ==========================================
# CHANGE PASSWORD REQUEST
# ==========================================

class ChangePasswordRequest(BaseModel):

    model_config = {
        "str_strip_whitespace": True
    }

    current_password: str = Field(
        min_length=1,
        max_length=100
    )

    new_password: str = Field(
        min_length=6,
        max_length=100
    )


# ==========================================
# AUTH RESPONSE
# ==========================================

class AuthResponse(BaseModel):

    message: str

    access_token: str

    token_type: str = "bearer"

    student_id: int

    username: str

    student_name: str

    message: str = Field(
        min_length=1
    )

    context: Optional[dict] = None


# ==========================================
# CHAT RESPONSE
# ==========================================

class ChatResponse(BaseModel):

    response: str

    context: dict


# ==========================================
# DASHBOARD RESPONSE
# ==========================================

class DashboardResponse(BaseModel):

    student_name: str

    # ------------------------------
    # ACADEMIC
    # ------------------------------

    average: float

    attendance: float

    performance_status: str

    # ------------------------------
    # RISK
    # ------------------------------

    risk_level: str

    risk_probability: float

    # ------------------------------
    # SUBJECT PERFORMANCE
    # ------------------------------

    highest_subject: str

    highest_mark: float

    lowest_subject: str

    lowest_mark: float

    # ------------------------------
    # TREND
    # ------------------------------

    overall_trend: str

    average_improvement: float

    # ------------------------------
    # RECOMMENDATION
    # ------------------------------

    recommendation: str

    priority_subject: str

    priority_mark: float


# ==========================================
# REGISTER REQUEST
# ==========================================

class RegisterRequest(BaseModel):

    model_config = {
        "str_strip_whitespace": True
    }

    student_id: int = Field(
        gt=0
    )

    username: str = Field(
        min_length=3,
        max_length=50
    )

    password: str = Field(
        min_length=6,
        max_length=100
    )


# ==========================================
# LOGIN REQUEST
# ==========================================

class LoginRequest(BaseModel):

    model_config = {
        "str_strip_whitespace": True
    }

    username: str = Field(
        min_length=1,
        max_length=50
    )

    password: str = Field(
        min_length=1,
        max_length=100
    )


# ==========================================
# AUTH RESPONSE
# ==========================================

class AuthResponse(BaseModel):

    message: str

    access_token: str

    token_type: str = "bearer"

    student_id: int

    username: str

    student_name: str