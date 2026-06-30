import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.utils import timezone
from django.contrib import messages

from .models import EmployeeProfile, CompanyInvite, ReferralRequest, ReferralNotification, ChatMessage
from .forms import EmployeeSignupForm, OTPVerificationForm, ReferralRequestForm, ReferralStageForm, ChatMessageForm
from .utils import extract_text_from_resume, extract_keywords_from_text, match_employees_to_keywords
from .emails import (
    send_otp_email, send_referral_request_email,
    send_referral_response_email, send_stage_update_email, send_viral_invite_nudge
)


# ─────────────────────────────────────────────────────────────────────────────
# EMPLOYEE SIDE
# ─────────────────────────────────────────────────────────────────────────────

@login_required
def employee_signup(request):
    """Employee self-registration: fill in profile, send OTP to work email."""
    # If already registered and verified, go to dashboard
    if hasattr(request.user, 'employee_profile'):
        if request.user.employee_profile.is_verified:
            return redirect('employee_dashboard')

    # Pre-fill company from invite link (stored in session)
    initial = {}
    invite_company = request.session.get('invite_company')
    invite_domain = request.session.get('invite_domain')
    if invite_company:
        initial['company'] = invite_company

    if request.method == 'POST':
        form = EmployeeSignupForm(request.POST)
        if form.is_valid():
            work_email = form.cleaned_data['work_email']

            # Validate work email domain matches invite domain if provided
            if invite_domain:
                email_domain = work_email.split('@')[-1].lower()
                if email_domain != invite_domain.lower():
                    form.add_error('work_email', f'Your work email must be from @{invite_domain}')
                    return render(request, 'referrals/employee_signup.html', {'form': form})

            # Check if this work email is already taken
            if EmployeeProfile.objects.filter(work_email=work_email).exclude(user=request.user).exists():
                form.add_error('work_email', 'An employee with this work email already exists.')
                return render(request, 'referrals/employee_signup.html', {'form': form})

            # Get or create profile for this user
            profile, _ = EmployeeProfile.objects.get_or_create(user=request.user)
            profile.company = form.cleaned_data['company']
            profile.job_title = form.cleaned_data['job_title']
            profile.department = form.cleaned_data['department']
            profile.work_email = work_email
            profile.domain_tags = form.cleaned_data['domain_tags_input']
            profile.is_verified = False
            profile.save()

            # Generate OTP and send
            otp = profile.generate_otp()
            send_otp_email(profile)

            messages.success(request, f'A 6-digit code has been sent to {work_email}. Please check your inbox.')
            return redirect('verify_work_email')
    else:
        form = EmployeeSignupForm(initial=initial)

    return render(request, 'referrals/employee_signup.html', {'form': form})


@login_required
def verify_work_email(request):
    """Employee enters the OTP sent to their work email."""
    try:
        profile = request.user.employee_profile
    except EmployeeProfile.DoesNotExist:
        return redirect('employee_signup')

    if profile.is_verified:
        return redirect('employee_dashboard')

    if request.method == 'POST':
        form = OTPVerificationForm(request.POST)
        if form.is_valid():
            otp_entered = form.cleaned_data['otp']
            if profile.verify_otp(otp_entered):
                messages.success(request, 'Your work email has been verified! Welcome to HirePilot Referrals.')
                # Clear invite session data
                request.session.pop('invite_company', None)
                request.session.pop('invite_domain', None)
                return redirect('employee_dashboard')
            else:
                messages.error(request, 'Invalid or expired code. Please try again or request a new one.')
    else:
        form = OTPVerificationForm()

    return render(request, 'referrals/verify_otp.html', {'form': form, 'work_email': profile.work_email})


@login_required
def resend_otp(request):
    """Resend the OTP to the employee's work email."""
    try:
        profile = request.user.employee_profile
    except EmployeeProfile.DoesNotExist:
        return redirect('employee_signup')
    profile.generate_otp()
    send_otp_email(profile)
    messages.success(request, 'A new verification code has been sent to your work email.')
    return redirect('verify_work_email')


@login_required
def employee_dashboard(request):
    """Employee sees all pending/accepted/declined referral requests."""
    try:
        profile = request.user.employee_profile
    except EmployeeProfile.DoesNotExist:
        return redirect('employee_signup')

    if not profile.is_verified:
        messages.warning(request, 'Please verify your work email first.')
        return redirect('verify_work_email')

    requests_qs = ReferralRequest.objects.filter(employee=profile).select_related('seeker').order_by('-created_at')
    pending = requests_qs.filter(status='pending')
    accepted = requests_qs.filter(status='accepted')
    declined = requests_qs.filter(status='declined')

    unread_notifications = ReferralNotification.objects.filter(
        recipient=request.user, is_read=False
    ).count()

    context = {
        'profile': profile,
        'pending_requests': pending,
        'accepted_requests': accepted,
        'declined_requests': declined,
        'total_requests': requests_qs.count(),
        'completed_count': profile.referrals_completed,
        'unread_count': unread_notifications,
    }
    return render(request, 'referrals/employee_dashboard.html', context)


@login_required
@require_POST
def respond_to_referral(request, pk):
    """Employee accepts or declines a referral request."""
    referral = get_object_or_404(ReferralRequest, pk=pk, employee__user=request.user)
    action = request.POST.get('action')  # 'accept' or 'decline'

    if action == 'accept':
        referral.status = 'accepted'
        referral.responded_at = timezone.now()
        referral.save(update_fields=['status', 'responded_at'])

        # Create in-app notification for seeker
        ReferralNotification.objects.create(
            recipient=referral.seeker,
            referral_request=referral,
            notification_type='accepted',
            message=f'{referral.employee.display_name} at {referral.employee.company} accepted your referral request!'
        )
        send_referral_response_email(referral)
        messages.success(request, f'You accepted the request from {referral.seeker.get_full_name() or referral.seeker.username}. A chat thread has been opened.')

    elif action == 'decline':
        referral.status = 'declined'
        referral.responded_at = timezone.now()
        referral.save(update_fields=['status', 'responded_at'])

        ReferralNotification.objects.create(
            recipient=referral.seeker,
            referral_request=referral,
            notification_type='declined',
            message=f'{referral.employee.display_name} at {referral.employee.company} declined your referral request.'
        )
        send_referral_response_email(referral)
        messages.info(request, 'Referral request declined.')

    return redirect('employee_dashboard')


@login_required
@require_POST
def update_referral_stage(request, pk):
    """Employee updates the HR pipeline stage for an accepted referral."""
    referral = get_object_or_404(ReferralRequest, pk=pk, employee__user=request.user, status='accepted')
    form = ReferralStageForm(request.POST, instance=referral)
    if form.is_valid():
        referral = form.save(commit=False)
        referral.stage_updated_at = timezone.now()
        referral.save(update_fields=['stage', 'stage_updated_at'])

        # Increment employee completed count on hire
        if referral.stage == 'hired':
            referral.employee.referrals_completed += 1
            referral.employee.save(update_fields=['referrals_completed'])
            send_viral_invite_nudge(referral.employee)

        stage_label = referral.get_stage_display_label()
        ReferralNotification.objects.create(
            recipient=referral.seeker,
            referral_request=referral,
            notification_type='stage_update',
            message=f'Your referral at {referral.employee.company} has been updated to: {stage_label}'
        )
        send_stage_update_email(referral)
        messages.success(request, f'Stage updated to: {stage_label}')

    return redirect('employee_dashboard')


@login_required
def invite_via_link(request, code):
    """Handle an employee invite link — pre-fill company info in session."""
    invite = get_object_or_404(CompanyInvite, invite_code=code)
    request.session['invite_company'] = invite.company_name
    request.session['invite_domain'] = invite.email_domain
    invite.used_count += 1
    invite.save(update_fields=['used_count'])
    messages.info(request, f'Welcome! You have been invited to join HirePilot as an employee from {invite.company_name}.')
    return redirect('employee_signup')


# ─────────────────────────────────────────────────────────────────────────────
# JOB SEEKER SIDE
# ─────────────────────────────────────────────────────────────────────────────

@login_required
def referral_marketplace(request):
    """Job seeker uploads resume, sees matched employees."""
    employees = []
    keywords = []
    resume_uploaded = False

    if request.method == 'POST' and request.FILES.get('resume'):
        resume_file = request.FILES['resume']
        text = extract_text_from_resume(resume_file)
        keywords = extract_keywords_from_text(text)
        employees = match_employees_to_keywords(keywords)
        resume_uploaded = True
        # Store resume file reference in session for follow-up request
        request.session['temp_resume_name'] = resume_file.name

    context = {
        'employees': employees,
        'keywords': keywords,
        'resume_uploaded': resume_uploaded,
    }
    return render(request, 'referrals/marketplace.html', context)


@login_required
def request_referral(request, employee_id):
    """Job seeker sends a referral request to a specific employee."""
    employee = get_object_or_404(EmployeeProfile, pk=employee_id, is_verified=True)

    # Prevent duplicate pending requests
    existing = ReferralRequest.objects.filter(
        seeker=request.user, employee=employee, status='pending'
    ).exists()
    if existing:
        messages.warning(request, f'You already have a pending request with {employee.display_name}.')
        return redirect('referral_marketplace')

    if request.method == 'POST':
        form = ReferralRequestForm(request.POST, request.FILES)
        if form.is_valid():
            referral = form.save(commit=False)
            referral.seeker = request.user
            referral.employee = employee
            referral.save()

            # Notify employee in-app
            ReferralNotification.objects.create(
                recipient=employee.user,
                referral_request=referral,
                notification_type='new_request',
                message=f'{request.user.get_full_name() or request.user.username} has sent you a referral request!'
            )
            send_referral_request_email(referral)
            messages.success(request, f'Your referral request has been sent to {employee.display_name} at {employee.company}!')
            return redirect('track_referrals')
    else:
        form = ReferralRequestForm()

    return render(request, 'referrals/request_referral.html', {'form': form, 'employee': employee})


@login_required
def track_referrals(request):
    """Job seeker views all their referral requests with a pipeline stepper."""
    referrals = ReferralRequest.objects.filter(
        seeker=request.user
    ).select_related('employee', 'employee__user').order_by('-created_at')

    total = referrals.count()
    pending = referrals.filter(status='pending').count()
    accepted = referrals.filter(status='accepted').count()
    declined = referrals.filter(status='declined').count()

    context = {
        'referrals': referrals,
        'total': total,
        'pending': pending,
        'accepted': accepted,
        'declined': declined,
    }
    return render(request, 'referrals/track_referrals.html', context)


# ─────────────────────────────────────────────────────────────────────────────
# CHAT
# ─────────────────────────────────────────────────────────────────────────────

@login_required
def chat_thread(request, referral_pk):
    """In-app chat thread between seeker and employee, only after acceptance."""
    referral = get_object_or_404(ReferralRequest, pk=referral_pk)

    # Only the seeker or the employee can access the chat
    is_seeker = referral.seeker == request.user
    is_employee = referral.employee.user == request.user
    if not (is_seeker or is_employee):
        messages.error(request, 'Access denied.')
        return redirect('referral_marketplace')

    if referral.status != 'accepted':
        messages.warning(request, 'Chat is only available after a referral request has been accepted.')
        return redirect('track_referrals')

    if request.method == 'POST':
        form = ChatMessageForm(request.POST)
        if form.is_valid():
            ChatMessage.objects.create(
                referral_request=referral,
                sender=request.user,
                body=form.cleaned_data['body']
            )
            return redirect('chat_thread', referral_pk=referral_pk)
    else:
        form = ChatMessageForm()

    chat_messages = referral.messages.select_related('sender').all()
    other_user = referral.employee.user if is_seeker else referral.seeker

    context = {
        'referral': referral,
        'chat_messages': chat_messages,
        'form': form,
        'is_seeker': is_seeker,
        'other_user': other_user,
    }
    return render(request, 'referrals/chat.html', context)


# ─────────────────────────────────────────────────────────────────────────────
# NOTIFICATIONS
# ─────────────────────────────────────────────────────────────────────────────

@login_required
def notifications_list(request):
    """In-app notification centre."""
    notifs = ReferralNotification.objects.filter(
        recipient=request.user
    ).select_related('referral_request').order_by('-created_at')
    # Mark all as read on page visit
    notifs.filter(is_read=False).update(is_read=True)
    return render(request, 'referrals/notifications.html', {'notifications': notifs})


@login_required
def mark_notification_read(request, pk):
    """AJAX endpoint to mark a single notification as read."""
    notif = get_object_or_404(ReferralNotification, pk=pk, recipient=request.user)
    notif.is_read = True
    notif.save(update_fields=['is_read'])
    return JsonResponse({'ok': True})


@login_required
def unread_notification_count(request):
    """AJAX endpoint — returns unread notification count as JSON."""
    count = ReferralNotification.objects.filter(
        recipient=request.user, is_read=False
    ).count()
    return JsonResponse({'count': count})
