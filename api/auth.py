from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from datetime import datetime, timedelta

from jose import jwt, JWTError

from passlib.context import CryptContext

import hashlib
import secrets
import os


# ==========================================
# PASSWORD HASHING
# ==========================================

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str
) -> bool:

    return pwd_context.verify(
        plain_password,
        hashed_password
    )


# ==========================================
# JWT CONFIGURATION
# ==========================================

SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "change_this_secret_key"
)

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 60


# ==========================================
# CREATE ACCESS TOKEN
# ==========================================

def create_access_token(data: dict):

    to_encode = data.copy()

    expire = (
        datetime.utcnow()
        + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    )

    to_encode.update(
        {
            "exp": expire
        }
    )

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


# ==========================================
# DECODE ACCESS TOKEN
# ==========================================

def decode_access_token(token: str):

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload

    except JWTError:

        return None


# ==========================================
# HTTP BEARER
# ==========================================

security = HTTPBearer()


# ==========================================
# GET CURRENT USER
# ==========================================

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(
        security
    )
):

    token = credentials.credentials

    payload = decode_access_token(token)

    if payload is None:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired authentication token.",
            headers={
                "WWW-Authenticate": "Bearer"
            }
        )

    student_id = payload.get(
        "student_id"
    )

    username = payload.get(
        "username"
    )

    if student_id is None or username is None:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token.",
            headers={
                "WWW-Authenticate": "Bearer"
            }
        )

    return {
        "user_id": payload.get("user_id"),
        "student_id": student_id,
        "username": username
    }


# ==========================================
# PASSWORD RESET
# ==========================================

RESET_CODE_EXPIRE_MINUTES = 10


def generate_reset_code() -> str:

    return f"{secrets.randbelow(1000000):06d}"


def hash_reset_code(
    code: str
) -> str:

    return hashlib.sha256(
        code.encode("utf-8")
    ).hexdigest()


def verify_reset_code(
    code: str,
    code_hash: str
) -> bool:

    calculated_hash = (
        hash_reset_code(code)
    )

    return secrets.compare_digest(
        calculated_hash,
        code_hash
    )


# ==========================================
# EMAIL VERIFICATION
# ==========================================

EMAIL_VERIFICATION_EXPIRE_MINUTES = 10


def generate_email_verification_code() -> str:

    return f"{secrets.randbelow(1000000):06d}"


def hash_email_verification_code(
    code: str
) -> str:

    return hashlib.sha256(
        code.encode("utf-8")
    ).hexdigest()


def verify_email_verification_code(
    code: str,
    code_hash: str
) -> bool:

    calculated_hash = (
        hash_email_verification_code(code)
    )

    return secrets.compare_digest(
        calculated_hash,
        code_hash
    )


# ==========================================
# PASSWORD CHANGE VERIFICATION
# ==========================================

PASSWORD_CHANGE_CODE_EXPIRE_MINUTES = 10


def generate_password_change_code() -> str:

    return f"{secrets.randbelow(1000000):06d}"


def hash_password_change_code(
    code: str
) -> str:

    return hashlib.sha256(
        code.encode("utf-8")
    ).hexdigest()


def verify_password_change_code(
    code: str,
    code_hash: str
) -> bool:

    calculated_hash = (
        hash_password_change_code(code)
    )

    return secrets.compare_digest(
        calculated_hash,
        code_hash
    )


# ==========================================
# EMAIL CHANGE VERIFICATION
# ==========================================

EMAIL_CHANGE_CODE_EXPIRE_MINUTES = 10


def generate_email_change_code() -> str:

    return f"{secrets.randbelow(1000000):06d}"


def hash_email_change_code(
    code: str
) -> str:

    return hashlib.sha256(
        code.encode("utf-8")
    ).hexdigest()


def verify_email_change_code(
    code: str,
    code_hash: str
) -> bool:

    calculated_hash = (
        hash_email_change_code(code)
    )

    return secrets.compare_digest(
        calculated_hash,
        code_hash
    )