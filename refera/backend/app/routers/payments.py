import hashlib
import hmac
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.database import get_db
from app.models import User, Subscription, SubscriptionPlan
from app.schemas import CreateOrderRequest, PaymentVerifyRequest
from app.auth.security import get_current_user
from app.config import get_settings

router = APIRouter(prefix="/payments", tags=["Payments"])
settings = get_settings()

PLANS = {
    "free": {"amount": 0, "referral_limit": settings.FREE_REFERRAL_LIMIT},
    "premium": {"amount": 99900, "referral_limit": settings.PREMIUM_REFERRAL_LIMIT},  # paise
}


@router.get("/plans")
def get_plans():
    return {
        "plans": [
            {
                "id": "free",
                "name": "Free",
                "price": 0,
                "currency": "INR",
                "features": ["3 referral requests/month", "Basic ATS score", "Job matching", "AI chatbot"],
                "referral_limit": settings.FREE_REFERRAL_LIMIT,
            },
            {
                "id": "premium",
                "name": "Premium",
                "price": 999,
                "currency": "INR",
                "period": "month",
                "features": [
                    "25 referral requests/month",
                    "Advanced ATS analysis",
                    "AI referral messages",
                    "Interview question generator",
                    "Priority support",
                ],
                "referral_limit": settings.PREMIUM_REFERRAL_LIMIT,
            },
        ]
    }


@router.post("/create-order")
def create_order(
    data: CreateOrderRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    plan = PLANS.get(data.plan)
    if not plan or data.plan == "free":
        raise HTTPException(status_code=400, detail="Invalid plan")

    if not settings.RAZORPAY_KEY_ID:
        return {
            "demo_mode": True,
            "order_id": f"demo_order_{current_user.id}_{data.plan}",
            "amount": plan["amount"],
            "currency": "INR",
            "key_id": "demo_key",
        }

    import razorpay
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    order = client.order.create({
        "amount": plan["amount"],
        "currency": "INR",
        "payment_capture": 1,
        "notes": {"user_id": str(current_user.id), "plan": data.plan},
    })
    return {"order_id": order["id"], "amount": plan["amount"], "currency": "INR", "key_id": settings.RAZORPAY_KEY_ID}


@router.post("/verify")
def verify_payment(
    data: PaymentVerifyRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if data.razorpay_order_id.startswith("demo_order_"):
        _activate_premium(db, current_user, data.razorpay_payment_id)
        return {"status": "success", "plan": "premium"}

    if not settings.RAZORPAY_KEY_SECRET:
        raise HTTPException(status_code=503, detail="Payment not configured")

    msg = f"{data.razorpay_order_id}|{data.razorpay_payment_id}"
    expected = hmac.new(
        settings.RAZORPAY_KEY_SECRET.encode(),
        msg.encode(),
        hashlib.sha256,
    ).hexdigest()

    if not hmac.compare_digest(expected, data.razorpay_signature):
        raise HTTPException(status_code=400, detail="Invalid payment signature")

    _activate_premium(db, current_user, data.razorpay_payment_id)
    return {"status": "success", "plan": "premium"}


def _activate_premium(db: Session, user: User, payment_id: str):
    user.subscription_plan = SubscriptionPlan.PREMIUM
    user.referral_limit = settings.PREMIUM_REFERRAL_LIMIT
    sub = Subscription(
        user_id=user.id,
        plan=SubscriptionPlan.PREMIUM,
        razorpay_payment_id=payment_id,
        amount=999.0,
        expires_at=datetime.utcnow() + timedelta(days=30),
    )
    db.add(sub)
    db.commit()
