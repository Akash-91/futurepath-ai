from urllib.parse import urlencode
from uuid import UUID
import secrets

from fastapi import Depends, FastAPI, HTTPException, Request, Response, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import or_, select
from sqlalchemy.orm import Session
from authlib.integrations.starlette_client import OAuth

from .config import settings
from .db import Base, engine, get_db
from .models.core import User
from .models.career import CareerProfile
from .schemas import CareerProfileRequest, CareerProfileResponse, RegisterRequest, UserResponse
from .security import create_access_token, decode_access_token, hash_password, verify_password

app = FastAPI(title="FuturePath AI API", version="0.3.0")
app.add_middleware(
    SessionMiddleware,
    secret_key=settings.jwt_secret,
    same_site="lax",
    https_only=settings.cookie_secure,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "OPTIONS"],
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


def set_session_cookie(response: Response, user_id: UUID) -> None:
    token = create_access_token(str(user_id))
    response.set_cookie(
        key=settings.auth_cookie_name,
        value=token,
        httponly=True,
        secure=settings.cookie_secure,
        samesite="lax",
        max_age=settings.jwt_expire_minutes * 60,
        path="/",
    )


def get_current_user(request: Request, db: Session) -> User:
    token = request.cookies.get(settings.auth_cookie_name)
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated.")
    user_id = decode_access_token(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Session expired. Please sign in again.")
    try:
        user = db.get(User, UUID(user_id))
    except ValueError:
        user = None
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="User account is unavailable.")
    return user


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
    user = User(
        username=username,
        email=email,
        password_hash=hash_password(payload.password),
        auth_provider="password",
        auth_subject=username,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@app.post("/auth/login")
def login(response: Response, form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    identity = form.username.strip()
    user = db.scalar(select(User).where(or_(User.username == identity, User.email == identity.lower())))
    if not user or not user.is_active or not user.password_hash or not verify_password(form.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username/email or password.")
    set_session_cookie(response, user.id)
    return {"authenticated": True, "user": UserResponse.model_validate(user)}


@app.get("/auth/google/login")
async def google_login(request: Request):
    if not settings.google_client_id or not settings.google_client_secret:
        raise HTTPException(status_code=503, detail="Google SSO is not configured on this deployment.")
    redirect_uri = f"{settings.backend_url.rstrip('/')}/auth/google/callback"
    return await oauth.google.authorize_redirect(request, redirect_uri)


@app.get("/auth/google/callback")
async def google_callback(request: Request, db: Session = Depends(get_db)):
    if not settings.google_client_id or not settings.google_client_secret:
        raise HTTPException(status_code=503, detail="Google SSO is not configured on this deployment.")
    try:
        token = await oauth.google.authorize_access_token(request)
        info = token.get("userinfo")
        if not info:
            info = await oauth.google.userinfo(token=token)
    except Exception:
        raise HTTPException(status_code=401, detail="Google sign-in could not be verified. Please try again.")

    email = (info.get("email") or "").lower().strip()
    subject = str(info.get("sub") or "").strip()
    if not email or not info.get("email_verified", False) or not subject:
        raise HTTPException(status_code=403, detail="A verified Google identity is required.")

    user = db.scalar(select(User).where(User.auth_provider == "google", User.auth_subject == subject))
    if not user:
        user = db.scalar(select(User).where(User.email == email))

    if not user:
        base_username = (email.split("@")[0] or "futurepath")[:70]
        username = base_username
        suffix = 1
        while db.scalar(select(User).where(User.username == username)):
            suffix += 1
            username = f"{base_username[:70-len(str(suffix))]}{suffix}"
        user = User(
            username=username,
            email=email,
            password_hash=hash_password(secrets.token_urlsafe(48)),
            auth_provider="google",
            auth_subject=subject,
        )
        db.add(user)
    else:
        user.email = email
        if user.auth_provider == "google":
            user.auth_subject = subject
        elif user.auth_provider == "password":
            # Preserve an existing password account while recording the verified Google identity.
            # The MVP keeps one primary provider per user; a future auth-identity table can support linking.
            pass
    db.commit()
    db.refresh(user)

    response = RedirectResponse(url=f"{settings.frontend_url.rstrip('/')}/welcome")
    set_session_cookie(response, user.id)
    return response


@app.get("/auth/me", response_model=UserResponse)
def current_user(request: Request, db: Session = Depends(get_db)):
    return get_current_user(request, db)


@app.get("/career-profile", response_model=CareerProfileResponse | None)
def get_career_profile(request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    return db.scalar(select(CareerProfile).where(CareerProfile.user_id == user.id))


@app.put("/career-profile", response_model=CareerProfileResponse)
def upsert_career_profile(payload: CareerProfileRequest, request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    profile = db.scalar(select(CareerProfile).where(CareerProfile.user_id == user.id))
    if not profile:
        profile = CareerProfile(user_id=user.id, **payload.model_dump())
        db.add(profile)
    else:
        for key, value in payload.model_dump().items():
            setattr(profile, key, value)
    db.commit()
    db.refresh(profile)
    return profile


@app.post("/auth/logout")
def logout(response: Response):
    response.delete_cookie(key=settings.auth_cookie_name, path="/")
    return {"authenticated": False}
