from urllib.parse import urlencode
from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import or_, select
from sqlalchemy.orm import Session
from authlib.integrations.starlette_client import OAuth

from .config import settings
from .db import Base, engine, get_db
from .models import User
from .schemas import RegisterRequest, UserResponse
from .security import create_access_token, hash_password, verify_password

Base.metadata.create_all(bind=engine)

app = FastAPI(title="FuturePath AI API", version="0.1.0")
app.add_middleware(SessionMiddleware, secret_key=settings.jwt_secret, same_site="lax", https_only=False)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)

oauth = OAuth()
if settings.google_client_id and settings.google_client_secret:
    oauth.register(
        name="google",
        client_id=settings.google_client_id,
        client_secret=settings.google_client_secret,
        server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
        client_kwargs={"scope": "openid email profile"},
    )

@app.get("/health")
def health():
    return {"status": "ok", "service": "futurepath-ai-api"}

@app.post("/auth/register", response_model=UserResponse, status_code=201)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    username = payload.username.strip()
    email = payload.email.lower().strip()
    exists = db.scalar(select(User).where(or_(User.username == username, User.email == email)))
    if exists:
        raise HTTPException(status_code=409, detail="Username or email is already registered.")
    user = User(username=username, email=email, password_hash=hash_password(payload.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@app.post("/auth/login")
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    identity = form.username.strip()
    user = db.scalar(select(User).where(or_(User.username == identity, User.email == identity.lower())))
    if not user or not user.is_active or not verify_password(form.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username/email or password.")
    token = create_access_token(str(user.id))
    return {"access_token": token, "token_type": "bearer", "expires_in": settings.jwt_expire_minutes * 60}

@app.get("/auth/google/login")
async def google_login(request: Request):
    if not settings.google_client_id or not settings.google_client_secret:
        raise HTTPException(status_code=503, detail="Google SSO is not configured. Add GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET to backend/.env.")
    redirect_uri = f"{settings.backend_url.rstrip('/')}/auth/google/callback"
    return await oauth.google.authorize_redirect(request, redirect_uri)

@app.get("/auth/google/callback")
async def google_callback(request: Request, db: Session = Depends(get_db)):
    if not settings.google_client_id or not settings.google_client_secret:
        raise HTTPException(status_code=503, detail="Google SSO is not configured.")
    try:
        token = await oauth.google.authorize_access_token(request)
        info = token.get("userinfo")
        if not info:
            info = await oauth.google.userinfo(token=token)
    except Exception:
        raise HTTPException(status_code=401, detail="Google sign-in could not be verified. Please try again.")
    email = (info.get("email") or "").lower().strip()
    if not email or not info.get("email_verified", False):
        raise HTTPException(status_code=403, detail="A verified Google email is required.")
    user = db.scalar(select(User).where(User.email == email))
    if not user:
        # MVP policy: provision an account for a verified Google identity.
        base_username = (email.split("@")[0] or "futurepath")[:70]
        username = base_username
        suffix = 1
        while db.scalar(select(User).where(User.username == username)):
            suffix += 1
            username = f"{base_username[:70-len(str(suffix))]}{suffix}"
        user = User(username=username, email=email, password_hash=hash_password(__import__("secrets").token_urlsafe(48)))
        db.add(user)
        db.commit()
        db.refresh(user)
    jwt_token = create_access_token(str(user.id))
    # For production, exchange this via a short-lived, one-time code or set an HttpOnly cookie.
    # Query-string tokens are a local-MVP convenience and should not be used in production.
    return RedirectResponse(f"{settings.frontend_url.rstrip('/')}/welcome?token={jwt_token}")
