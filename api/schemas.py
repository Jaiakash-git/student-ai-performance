from pydantic import BaseModel, Field
from typing import Optional


# ==========================================
# CHAT REQUEST
# ==========================================

class ChatRequest(BaseModel):

    model_config = {
        "str_strip_whitespace": True
    }

    student_name: str = Field(min_length=1)
    message: str = Field(min_length=1)
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
