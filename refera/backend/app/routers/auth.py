from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime

from app.database import get_db
from app.models import User, UserRole, SubscriptionPlan
from app.schemas import UserRegister, UserLogin, Token, UserOut, GoogleAuthRequest
from app.auth.security import (
    get_password_hash, verify_password, create_access_token, get_current_user,
)
from app.config import get_settings

router = APIRouter(prefix="/auth", tags=["Authentication"])
settings = get_settings()


def _user_out(user: User) -> UserOut:
    return UserOut(
        id=user.id,
        email=user.email,
        full_name=user.full_name,
        role=user.role.value,
        avatar_url=user.avatar_url,
        company=user.company,
        job_title=user.job_title,
        bio=user.bio,
        location=user.location,
        linkedin_url=user.linkedin_url,
        subscription_plan=user.subscription_plan.value,
        referral_limit=user.referral_limit,
        referrals_used=user.referrals_used,
        created_at=user.created_at,
    )


@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
def register(data: UserRegister, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    role_map = {"candidate": UserRole.CANDIDATE, "employee": UserRole.EMPLOYEE, "admin": UserRole.ADMIN}
    role = role_map.get(data.role, UserRole.CANDIDATE)

    user = User(
        email=data.email,
        hashed_password=get_password_hash(data.password),
        full_name=data.full_name,
        role=role,
        referral_limit=settings.FREE_REFERRAL_LIMIT,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_access_token({"sub": str(user.id)})
    return Token(access_token=token, user=_user_out(user))


@router.post("/login", response_model=Token)
def login(data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not user.hashed_password or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token({"sub": str(user.id)})
    return Token(access_token=token, user=_user_out(user))


@router.get("/me", response_model=UserOut)
def get_me(current_user: User = Depends(get_current_user)):
    return _user_out(current_user)


@router.post("/google", response_model=Token)
async def google_auth(data: GoogleAuthRequest, db: Session = Depends(get_db)):
    """Verify Google ID token and create/login user."""
    import httpx

    if not settings.GOOGLE_CLIENT_ID:
        raise HTTPException(status_code=503, detail="Google OAuth not configured")

    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"https://oauth2.googleapis.com/tokeninfo?id_token={data.id_token}"
        )
        if resp.status_code != 200:
            raise HTTPException(status_code=401, detail="Invalid Google token")
        info = resp.json()

    if info.get("aud") != settings.GOOGLE_CLIENT_ID:
        raise HTTPException(status_code=401, detail="Token audience mismatch")

    email = info["email"]
    google_id = info["sub"]
    name = info.get("name", email.split("@")[0])
    avatar = info.get("picture")

    user = db.query(User).filter(
        (User.google_id == google_id) | (User.email == email)
    ).first()

    if user:
        user.google_id = google_id
        user.avatar_url = avatar or user.avatar_url
        user.updated_at = datetime.utcnow()
    else:
        user = User(
            email=email,
            full_name=name,
            google_id=google_id,
            avatar_url=avatar,
            role=UserRole.CANDIDATE,
            referral_limit=settings.FREE_REFERRAL_LIMIT,
        )
        db.add(user)

    db.commit()
    db.refresh(user)
    token = create_access_token({"sub": str(user.id)})
    return Token(access_token=token, user=_user_out(user))
