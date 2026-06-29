from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import User
from app.schemas import UserUpdate, UserOut
from app.auth.security import get_current_user

router = APIRouter(prefix="/users", tags=["Users"])


def _user_out(user: User) -> UserOut:
    return UserOut(
        id=user.id, email=user.email, full_name=user.full_name, role=user.role.value,
        avatar_url=user.avatar_url, company=user.company, job_title=user.job_title,
        bio=user.bio, location=user.location, linkedin_url=user.linkedin_url,
        subscription_plan=user.subscription_plan.value,
        referral_limit=user.referral_limit, referrals_used=user.referrals_used,
        created_at=user.created_at,
    )


@router.put("/profile", response_model=UserOut)
def update_profile(data: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(current_user, field, value)
    db.commit()
    db.refresh(current_user)
    return _user_out(current_user)


@router.get("/employees", response_model=List[UserOut])
def list_employees(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    from app.models import UserRole
    employees = db.query(User).filter(User.role == UserRole.EMPLOYEE, User.is_active == True).all()
    return [_user_out(e) for e in employees]


@router.get("/{user_id}", response_model=UserOut)
def get_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return _user_out(user)
