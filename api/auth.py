# ==========================================
# AUTHENTICATION UTILITIES
# ==========================================

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
import os


# ==========================================
# PASSWORD HASHING
# ==========================================

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def hash_password(password: str):
    """
    Hash a plain password before storing it
    in the database.
    """

    return pwd_context.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str
):
    """
    Verify a plain password against
    the stored hashed password.
    """

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
# CREATE JWT TOKEN
# ==========================================

def create_access_token(data: dict):
    """
    Create a JWT access token.
    """

    token_data = data.copy()

    expire = (
        datetime.utcnow()
        + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    )

    token_data.update(
        {
            "exp": expire
        }
    )

    encoded_jwt = jwt.encode(
        token_data,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt


# ==========================================
# DECODE JWT TOKEN
# ==========================================

def decode_access_token(token: str):
    """
    Decode and verify a JWT access token.
    """

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
# HTTP BEARER SECURITY
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
    """
    Extract the JWT token from the Authorization
    header, verify it, and return the authenticated
    user's information.
    """

    token = credentials.credentials

    payload = decode_access_token(token)

    # --------------------------------------
    # INVALID / EXPIRED TOKEN
    # --------------------------------------

    if payload is None:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token.",
            headers={
                "WWW-Authenticate": "Bearer"
            }
        )

    # --------------------------------------
    # GET USER INFORMATION
    # --------------------------------------

    student_id = payload.get(
        "student_id"
    )

    username = payload.get(
        "username"
    )

    # --------------------------------------
    # VALIDATE TOKEN DATA
    # --------------------------------------

    if (
        student_id is None
        or username is None
    ):

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token.",
            headers={
                "WWW-Authenticate": "Bearer"
            }
        )

    # --------------------------------------
    # RETURN CURRENT USER
    # --------------------------------------

    return {
        "student_id": student_id,
        "username": username
    }