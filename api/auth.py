# ==========================================
# AUTHENTICATION UTILITIES
# ==========================================

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
    Decode and verify a JWT token.
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