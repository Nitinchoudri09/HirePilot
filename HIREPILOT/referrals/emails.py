from django.conf import settings
from Home.email_utils import send_brevo_email


def send_otp_email(employee):
    """Send a 6-digit OTP to the employee's work email for verification."""
    subject = 'HirePilot — Verify your work email'
    html_content = f"""
    <p>Hi {employee.display_name},</p>
    <p>Your verification code for HirePilot is:</p>
    <h2 style="color: #3b82f6; font-size: 24px; font-weight: 700;">{employee.otp_token}</h2>
    <p>This code expires in 15 minutes.</p>
    <p>If you did not sign up for HirePilot, you can safely ignore this email.</p>
    <p>— The HirePilot Team</p>
    """
    return send_brevo_email(
        to_email=employee.work_email,
        to_name=employee.display_name,
        subject=subject,
        html_content=html_content
    )


def send_referral_request_email(referral_request):
    """Notify the employee of a new referral request from a seeker."""
    emp_user = referral_request.employee.user
    seeker = referral_request.seeker
    subject = f'HirePilot — New Referral Request from {seeker.get_full_name() or seeker.username}'
    html_content = f"""
    <p>Hi {referral_request.employee.display_name},</p>
    <p><strong>{seeker.get_full_name() or seeker.username}</strong> has sent you a referral request on HirePilot.</p>
    <p>Note from them:</p>
    <blockquote style="border-left: 4px solid #3b82f6; padding-left: 16px; margin: 16px 0; color: #555; font-style: italic;">
        "{referral_request.note or 'No note provided.'}"
    </blockquote>
    <p>Log in to your dashboard to review and respond:</p>
    <p><a href="{settings.SITE_URL}/referrals/employee/dashboard/" style="display: inline-block; padding: 10px 20px; background-color: #3b82f6; color: white; text-decoration: none; border-radius: 6px; font-weight: 600;">View Dashboard</a></p>
    <p>— The HirePilot Team</p>
    """
    recipient_email = emp_user.email or referral_request.employee.work_email
    return send_brevo_email(
        to_email=recipient_email,
        to_name=referral_request.employee.display_name,
        subject=subject,
        html_content=html_content
    )


def send_referral_response_email(referral_request):
    """Notify the seeker that their request was accepted or declined."""
    seeker = referral_request.seeker
    employee = referral_request.employee
    status = referral_request.status.capitalize()
    subject = f'HirePilot — Your referral request was {status}'
    if referral_request.status == 'accepted':
        action_line = f"Great news! <strong>{employee.display_name}</strong> at <strong>{employee.company}</strong> has accepted your referral request. You can now chat with them on HirePilot."
    else:
        action_line = f"<strong>{employee.display_name}</strong> at <strong>{employee.company}</strong> has declined your referral request. Don't give up — there are other employees you can reach out to!"
    
    html_content = f"""
    <p>Hi {seeker.get_full_name() or seeker.username},</p>
    <p>{action_line}</p>
    <p>View your referrals dashboard:</p>
    <p><a href="{settings.SITE_URL}/referrals/track/" style="display: inline-block; padding: 10px 20px; background-color: #3b82f6; color: white; text-decoration: none; border-radius: 6px; font-weight: 600;">Track Referrals</a></p>
    <p>— The HirePilot Team</p>
    """
    return send_brevo_email(
        to_email=seeker.email,
        to_name=seeker.get_full_name() or seeker.username,
        subject=subject,
        html_content=html_content
    )


def send_stage_update_email(referral_request):
    """Notify the seeker when the referral pipeline stage changes."""
    seeker = referral_request.seeker
    employee = referral_request.employee
    stage_label = referral_request.get_stage_display_label()
    subject = f'HirePilot — Referral Update: {stage_label}'
    html_content = f"""
    <p>Hi {seeker.get_full_name() or seeker.username},</p>
    <p><strong>{employee.display_name}</strong> at <strong>{employee.company}</strong> has updated your referral status to:</p>
    <h3 style="color: #3b82f6;">➤ {stage_label}</h3>
    <p>Track your full referral progress here:</p>
    <p><a href="{settings.SITE_URL}/referrals/track/" style="display: inline-block; padding: 10px 20px; background-color: #3b82f6; color: white; text-decoration: none; border-radius: 6px; font-weight: 600;">Track Progress</a></p>
    <p>— The HirePilot Team</p>
    """
    return send_brevo_email(
        to_email=seeker.email,
        to_name=seeker.get_full_name() or seeker.username,
        subject=subject,
        html_content=html_content
    )


def send_viral_invite_nudge(employee):
    """After completing a referral, invite employee to bring a teammate."""
    subject = 'HirePilot — Invite a teammate to help others'
    invite_url = employee.user.employee_profile.invite_link if hasattr(employee.user, 'employee_profile') else settings.SITE_URL + '/referrals/employee/signup/'
    html_content = f"""
    <p>Hi {employee.display_name},</p>
    <p>You've now helped <strong>{employee.referrals_completed}</strong> job seeker(s) get a referral — that's amazing! 🎉</p>
    <p>Would you like to invite a teammate at <strong>{employee.company}</strong> to also help candidates on HirePilot?</p>
    <p>Share this link with them:</p>
    <p><a href="{invite_url}" style="display: inline-block; padding: 10px 20px; background-color: #8b5cf6; color: white; text-decoration: none; border-radius: 6px; font-weight: 600;">Invite Teammate</a></p>
    <p>Thank you for making a difference!</p>
    <p>— The HirePilot Team</p>
    """
    return send_brevo_email(
        to_email=employee.work_email,
        to_name=employee.display_name,
        subject=subject,
        html_content=html_content
    )
