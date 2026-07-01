import uuid
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class EmployeeProfile(models.Model):
    """An employee who has self-registered and been verified via work email OTP."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee_profile')
    company = models.CharField(max_length=255)
    job_title = models.CharField(max_length=255)
    department = models.CharField(max_length=255, blank=True)
    work_email = models.EmailField(unique=True)
    domain_tags = models.JSONField(default=list, help_text="List of skill/domain keywords, e.g. ['Python', 'Backend', 'Django']")
    is_verified = models.BooleanField(default=True)
    otp_token = models.CharField(max_length=6, blank=True)
    otp_expires_at = models.DateTimeField(null=True, blank=True)
    invited_by = models.ForeignKey(
        'self', null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='invitees'
    )
    referrals_completed = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} @ {self.company}"

    @property
    def display_name(self):
        return self.user.get_full_name() or self.user.username

    def generate_otp(self):
        import random
        self.otp_token = str(random.randint(100000, 999999))
        self.otp_expires_at = timezone.now() + timezone.timedelta(minutes=15)
        self.save(update_fields=['otp_token', 'otp_expires_at'])
        return self.otp_token

    def verify_otp(self, token):
        if (self.otp_token == token and
                self.otp_expires_at and
                timezone.now() <= self.otp_expires_at):
            self.is_verified = True
            self.otp_token = ''
            self.otp_expires_at = None
            self.save(update_fields=['is_verified', 'otp_token', 'otp_expires_at'])
            return True
        return False


class CompanyInvite(models.Model):
    """Shareable invite link that pre-fills company info on employee signup."""
    company_name = models.CharField(max_length=255)
    email_domain = models.CharField(max_length=255, help_text="e.g. google.com")
    invite_code = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_invites')
    used_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Invite for {self.company_name} ({self.email_domain})"

    @property
    def invite_link(self):
        from django.conf import settings
        return f"{settings.SITE_URL}/referrals/invite/{self.invite_code}/"


class ReferralRequest(models.Model):
    """A job seeker's request for a referral from a verified employee."""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
    ]
    STAGE_CHOICES = [
        ('', 'Not Submitted Yet'),
        ('submitted', 'Submitted to HR'),
        ('shortlisted', 'Shortlisted'),
        ('interview', 'Interview Scheduled'),
        ('hired', 'Hired 🎉'),
        ('rejected', 'Rejected'),
    ]

    seeker = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='referral_requests_sent'
    )
    employee = models.ForeignKey(
        EmployeeProfile, on_delete=models.CASCADE,
        related_name='referral_requests_received'
    )
    resume = models.FileField(upload_to='referral_resumes/')
    note = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    stage = models.CharField(max_length=20, choices=STAGE_CHOICES, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    responded_at = models.DateTimeField(null=True, blank=True)
    stage_updated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.seeker.username} → {self.employee} ({self.status})"

    def get_stage_display_label(self):
        return dict(self.STAGE_CHOICES).get(self.stage, '')


class ReferralNotification(models.Model):
    """In-app notification for referral events."""
    TYPE_CHOICES = [
        ('new_request', 'New Referral Request'),
        ('accepted', 'Request Accepted'),
        ('declined', 'Request Declined'),
        ('stage_update', 'Stage Updated'),
    ]
    recipient = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='referral_notifications'
    )
    referral_request = models.ForeignKey(
        ReferralRequest, on_delete=models.CASCADE,
        related_name='notifications'
    )
    notification_type = models.CharField(max_length=30, choices=TYPE_CHOICES)
    message = models.TextField(blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.notification_type} → {self.recipient.username}"


class ChatMessage(models.Model):
    """In-app chat messages between seeker and employee after acceptance."""
    referral_request = models.ForeignKey(
        ReferralRequest, on_delete=models.CASCADE,
        related_name='messages'
    )
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['sent_at']

    def __str__(self):
        return f"{self.sender.username}: {self.body[:50]}"
