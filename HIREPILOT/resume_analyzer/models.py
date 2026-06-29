from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta


class SubscriptionPlan(models.Model):
    PLAN_TYPES = [
        ('basic', 'Basic'),
        ('premium', 'Premium'),
    ]
    name        = models.CharField(max_length=50)
    plan_type   = models.CharField(max_length=20, choices=PLAN_TYPES, unique=True)
    price       = models.DecimalField(max_digits=8, decimal_places=2)
    credits     = models.PositiveIntegerField(help_text="Number of resume analyses allowed")
    validity_days = models.PositiveIntegerField(default=30)
    description = models.TextField(blank=True)
    is_active   = models.BooleanField(default=True)
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} – ₹{self.price}"

    class Meta:
        ordering = ['price']


class UserSubscription(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
    ]
    user            = models.OneToOneField(User, on_delete=models.CASCADE, related_name='subscription')
    plan            = models.ForeignKey(SubscriptionPlan, on_delete=models.SET_NULL, null=True)
    credits_remaining = models.PositiveIntegerField(default=2)
    start_date      = models.DateTimeField(auto_now_add=True)
    expiry_date     = models.DateTimeField(null=True, blank=True)
    status          = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    updated_at      = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} – {self.plan.name if self.plan else 'No Plan'}"

    @property
    def is_valid(self):
        if self.status != 'active':
            return False
        if self.expiry_date and timezone.now() > self.expiry_date:
            self.status = 'expired'
            self.save(update_fields=['status'])
            return False
        return True

    @property
    def days_remaining(self):
        if self.expiry_date:
            delta = self.expiry_date - timezone.now()
            return max(0, delta.days)
        return 0

    @property
    def usage_percentage(self):
        if self.plan and self.plan.credits > 0:
            used = self.plan.credits - self.credits_remaining
            return min(100, round((used / self.plan.credits) * 100))
        return 0

    class Meta:
        verbose_name = "User Subscription"


class Payment(models.Model):
    STATUS_CHOICES = [
        ('created', 'Created'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    user              = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    plan              = models.ForeignKey(SubscriptionPlan, on_delete=models.SET_NULL, null=True)
    razorpay_order_id = models.CharField(max_length=100, unique=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True)
    razorpay_signature  = models.CharField(max_length=255, blank=True)
    amount            = models.DecimalField(max_digits=10, decimal_places=2)
    currency          = models.CharField(max_length=10, default='INR')
    status            = models.CharField(max_length=20, choices=STATUS_CHOICES, default='created')
    created_at        = models.DateTimeField(auto_now_add=True)
    paid_at           = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} – ₹{self.amount} ({self.status})"

    class Meta:
        ordering = ['-created_at']


class ResumeAnalysisHistory(models.Model):
    user       = models.ForeignKey(User, on_delete=models.CASCADE, related_name='analysis_history')
    job_title  = models.CharField(max_length=200, blank=True)
    ats_score  = models.FloatField()
    missing_keywords = models.JSONField(default=list)
    suggestions      = models.JSONField(default=list)
    detailed_report  = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} – {self.ats_score}% on {self.created_at.strftime('%d %b %Y')}"

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Resume Analysis"
        verbose_name_plural = "Resume Analyses"
