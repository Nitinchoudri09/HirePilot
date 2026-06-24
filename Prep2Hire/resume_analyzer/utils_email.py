from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone


def send_payment_confirmation(user, plan, payment):
    """Email sent after successful Razorpay payment."""
    try:
        subject = f"🎉 Payment Confirmed – {plan.name} Plan Activated | HirePilot"
        message = f"""Hi {user.first_name or user.username},

Your payment has been successfully processed!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  PAYMENT RECEIPT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Plan         : {plan.name}
  Amount Paid  : ₹{payment.amount}
  Order ID     : {payment.razorpay_order_id}
  Payment ID   : {payment.razorpay_payment_id}
  Date         : {payment.paid_at.strftime('%d %b %Y, %I:%M %p') if payment.paid_at else timezone.now().strftime('%d %b %Y')}
  Validity     : {plan.validity_days} days
  Credits      : {plan.credits} resume analyses
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

You can now analyze up to {plan.credits} resumes with our ATS engine.

Visit your dashboard: http://127.0.0.1:8000/resume-analyzer/subscription/

Thanks for choosing HirePilot! 🚀

– The HirePilot Team
"""
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=True,
        )
    except Exception:
        pass  # Never break the payment flow due to email errors


def send_low_credits_warning(user, remaining):
    """Email when only 1 credit remains."""
    try:
        subject = "⚠️ Low Credits Alert – Only 1 Analysis Left | HirePilot"
        message = f"""Hi {user.first_name or user.username},

You have only {remaining} resume analysis remaining on your current plan.

Don't miss out! Upgrade your plan to continue improving your resume and landing interviews.

👉 Upgrade now: http://127.0.0.1:8000/resume-analyzer/pricing/

– The HirePilot Team
"""
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=True,
        )
    except Exception:
        pass


def send_plan_expiry_warning(user, subscription):
    """Email when plan expires within 3 days."""
    try:
        subject = f"📅 Your {subscription.plan.name} Plan Expires Soon | HirePilot"
        message = f"""Hi {user.first_name or user.username},

Your {subscription.plan.name} plan expires on {subscription.expiry_date.strftime('%d %b %Y')}.

Renew now to keep your ATS analysis access uninterrupted.

👉 Renew: http://127.0.0.1:8000/resume-analyzer/pricing/

– The HirePilot Team
"""
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=True,
        )
    except Exception:
        pass
