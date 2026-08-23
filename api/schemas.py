from pydantic import BaseModel, Field
from typing import Optional


class ChatRequest(BaseModel):
    model_config = {
        "str_strip_whitespace": True
    }

    student_name: str = Field(min_length=1)
    message: str = Field(min_length=1)
    context: Optional[dict] = None


class ChatResponse(BaseModel):
    response: str
    context: dict