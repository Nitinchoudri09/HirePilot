from django.core.mail import send_mail
from django.conf import settings


def send_otp_email(employee):
    """Send a 6-digit OTP to the employee's work email for verification."""
    subject = 'HirePilot — Verify your work email'
    message = f"""Hi {employee.display_name},

Your verification code for HirePilot is:

    {employee.otp_token}

This code expires in 15 minutes.

If you did not sign up for HirePilot, you can safely ignore this email.

— The HirePilot Team"""
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[employee.work_email],
            fail_silently=False,
        )
        return True
    except Exception as e:
        import logging
        logging.getLogger('django').error(f'[HirePilot] OTP email failed: {e}')
        return False


def send_referral_request_email(referral_request):
    """Notify the employee of a new referral request from a seeker."""
    emp_user = referral_request.employee.user
    seeker = referral_request.seeker
    subject = f'HirePilot — New Referral Request from {seeker.get_full_name() or seeker.username}'
    message = f"""Hi {referral_request.employee.display_name},

{seeker.get_full_name() or seeker.username} has sent you a referral request on HirePilot.

Note from them:
"{referral_request.note or 'No note provided.'}"

Log in to your dashboard to review and respond:
{settings.SITE_URL}/referrals/employee/dashboard/

— The HirePilot Team"""
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[emp_user.email],
            fail_silently=True,
        )
    except Exception:
        pass


def send_referral_response_email(referral_request):
    """Notify the seeker that their request was accepted or declined."""
    seeker = referral_request.seeker
    employee = referral_request.employee
    status = referral_request.status.capitalize()
    subject = f'HirePilot — Your referral request was {status}'
    if referral_request.status == 'accepted':
        action_line = f"Great news! {employee.display_name} at {employee.company} has accepted your referral request. You can now chat with them on HirePilot."
    else:
        action_line = f"{employee.display_name} at {employee.company} has declined your referral request. Don't give up — there are other employees you can reach out to!"
    message = f"""Hi {seeker.get_full_name() or seeker.username},

{action_line}

View your referrals dashboard:
{settings.SITE_URL}/referrals/track/

— The HirePilot Team"""
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[seeker.email],
            fail_silently=True,
        )
    except Exception:
        pass


def send_stage_update_email(referral_request):
    """Notify the seeker when the referral pipeline stage changes."""
    seeker = referral_request.seeker
    employee = referral_request.employee
    stage_label = referral_request.get_stage_display_label()
    subject = f'HirePilot — Referral Update: {stage_label}'
    message = f"""Hi {seeker.get_full_name() or seeker.username},

{employee.display_name} at {employee.company} has updated your referral status to:

    ➤ {stage_label}

Track your full referral progress here:
{settings.SITE_URL}/referrals/track/

— The HirePilot Team"""
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[seeker.email],
            fail_silently=True,
        )
    except Exception:
        pass


def send_viral_invite_nudge(employee):
    """After completing a referral, invite employee to bring a teammate."""
    subject = 'HirePilot — Invite a teammate to help others'
    message = f"""Hi {employee.display_name},

You've now helped {employee.referrals_completed} job seeker(s) get a referral — that's amazing! 🎉

Would you like to invite a teammate at {employee.company} to also help candidates on HirePilot?

Share this link with them:
{employee.user.employee_profile.invite_link if hasattr(employee.user, 'employee_profile') else settings.SITE_URL + '/referrals/employee/signup/'}

Thank you for making a difference!

— The HirePilot Team"""
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[employee.work_email],
            fail_silently=True,
        )
    except Exception:
        pass
