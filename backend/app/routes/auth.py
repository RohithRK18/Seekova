import secrets
import hashlib
from typing import Dict, Any, Optional
from fastapi import APIRouter, HTTPException, Depends, Header
from pydantic import BaseModel, EmailStr

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

# Secure in-memory user database & tokens
USERS_DB: Dict[str, Dict[str, Any]] = {}
SESSIONS_DB: Dict[str, str] = {}
RESET_TOKENS: Dict[str, str] = {}

class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

class ForgotPasswordRequest(BaseModel):
    email: str

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

@router.post("/register")
async def register(req: RegisterRequest):
    email_clean = req.email.lower().strip()
    if email_clean in USERS_DB:
        raise HTTPException(status_code=400, detail="An account with this email already exists.")
    
    if len(req.password) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters long.")

    user = {
        "id": f"usr-{secrets.token_hex(4)}",
        "name": req.name.strip(),
        "email": email_clean,
        "password_hash": hash_password(req.password)
    }
    USERS_DB[email_clean] = user

    # Create session token
    token = secrets.token_hex(16)
    SESSIONS_DB[token] = email_clean

    return {
        "success": True,
        "message": "Account created successfully.",
        "token": token,
        "user": {"id": user["id"], "name": user["name"], "email": user["email"]}
    }

@router.post("/login")
async def login(req: LoginRequest):
    email_clean = req.email.lower().strip()
    user = USERS_DB.get(email_clean)
    
    if not user or user["password_hash"] != hash_password(req.password):
        raise HTTPException(status_code=401, detail="Invalid email or password.")

    token = secrets.token_hex(16)
    SESSIONS_DB[token] = email_clean

    return {
        "success": True,
        "token": token,
        "user": {"id": user["id"], "name": user["name"], "email": user["email"]}
    }

@router.post("/forgot-password")
async def forgot_password(req: ForgotPasswordRequest):
    email_clean = req.email.lower().strip()
    # Always return success to prevent user enumeration security attacks
    if email_clean in USERS_DB:
        reset_token = secrets.token_hex(20)
        RESET_TOKENS[reset_token] = email_clean
        print(f"[SECONDLYBRAIN AUTH EMAIL] Password Reset Link for {email_clean}: http://localhost:5173/?reset_token={reset_token}")
        
    return {
        "success": True,
        "message": "If an account exists for this email, a password reset link has been sent."
    }

@router.post("/reset-password")
async def reset_password(req: ResetPasswordRequest):
    email = RESET_TOKENS.get(req.token)
    if not email or email not in USERS_DB:
        raise HTTPException(status_code=400, detail="Invalid or expired reset token.")

    if len(req.new_password) < 6:
        raise HTTPException(status_code=400, detail="New password must be at least 6 characters long.")

    USERS_DB[email]["password_hash"] = hash_password(req.new_password)
    del RESET_TOKENS[req.token]

    return {
        "success": True,
        "message": "Password updated successfully. You can now log in."
    }

@router.get("/me")
async def get_current_user(authorization: Optional[str] = Header(None)):
    if not authorization:
        return {"user": None}
    
    token = authorization.replace("Bearer ", "").strip()
    email = SESSIONS_DB.get(token)
    if not email or email not in USERS_DB:
        return {"user": None}

    u = USERS_DB[email]
    return {
        "user": {"id": u["id"], "name": u["name"], "email": u["email"]}
    }

@router.post("/logout")
async def logout(authorization: Optional[str] = Header(None)):
    if authorization:
        token = authorization.replace("Bearer ", "").strip()
        if token in SESSIONS_DB:
            del SESSIONS_DB[token]
    return {"success": True}
