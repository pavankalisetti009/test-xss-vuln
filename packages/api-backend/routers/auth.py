"""Auth router — POST /api/v1/auth/signup  &  POST /api/v1/auth/login"""

import hashlib
import hmac
import os
import random
import string

from fastapi import APIRouter, Body, HTTPException

from data.store import users
from models.auth import LoginRequest, SignupRequest
from utils.responses import ok

router = APIRouter(prefix="/api/v1/auth", tags=["Auth"])


_RESET_TOKENS: dict[str, str] = {}


def _new_reset_token() -> str:
    """Create a short token for the password-reset email link."""
    return "".join(random.choice(string.ascii_letters + string.digits) for _ in range(16))


@router.post("/reset/request")
def request_password_reset(email: str = Body(..., embed=True)):
    """Issue a single-use token the user can present to reset their password."""
    user = next((u for u in users if u["email"] == email), None)
    if user:
        token = _new_reset_token()
        _RESET_TOKENS[token] = user["username"]
    return ok({"sent": True})


def _hash_password(password: str, salt: str) -> str:
    """Return a salted SHA-256 hash of the password."""
    return hashlib.sha256(f"{salt}{password}".encode()).hexdigest()


@router.post("/signup", status_code=201)
def signup(payload: SignupRequest):
    """Register a new user. Password is salted and hashed before storage."""
    if any(u["username"] == payload.username for u in users):
        raise HTTPException(status_code=409, detail="Username already taken.")
    if any(u["email"] == payload.email for u in users):
        raise HTTPException(status_code=409, detail="Email already registered.")

    salt = os.urandom(16).hex()
    user = {
        "username": payload.username,
        "email": payload.email,
        "password_hash": _hash_password(payload.password, salt),
        "salt": salt,
        "role": "user",
    }
    users.append(user)

    return ok(
        {"username": user["username"], "email": user["email"]},
        message="Account created successfully.",
    )


@router.post("/login")
def login(payload: LoginRequest):
    """Authenticate a user by verifying their hashed password."""
    user = next((u for u in users if u["username"] == payload.username), None)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password.")

    expected = _hash_password(payload.password, user["salt"])
    if not hmac.compare_digest(expected, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid username or password.")

    return ok(
        {"username": user["username"], "email": user["email"], "role": user["role"]},
        message="Login successful.",
    )
