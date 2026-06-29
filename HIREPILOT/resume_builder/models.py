from django.db import models
from django.contrib.auth.models import User

class UserSubscription(models.Model):
    PLAN_CHOICES = [
        ('FREE', 'Free Plan'),
        ('SILVER', 'Silver Plan'),
        ('GOLD', 'Gold Plan'),
        ('PREMIUM', 'Premium Plan'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='resume_subscription')
    plan = models.CharField(max_length=20, choices=PLAN_CHOICES, default='FREE')
    razorpay_customer_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_subscription_id = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.get_plan_display()}"

class ResumeTemplate(models.Model):
    PLAN_CHOICES = [
        ('FREE', 'Free'),
        ('SILVER', 'Silver'),
        ('GOLD', 'Gold'),
        ('PREMIUM', 'Premium'),
    ]
    name = models.CharField(max_length=100)  # e.g. "Software Engineer Resume"
    template_id = models.CharField(max_length=50, unique=True)  # e.g. "software_engineer"
    category = models.CharField(max_length=50) # e.g. "Professional", "Beginner"
    required_plan = models.CharField(max_length=20, choices=PLAN_CHOICES, default='FREE')
    thumbnail = models.ImageField(upload_to='resume_templates/', blank=True, null=True)
    usage_count = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resumes')
    title = models.CharField(max_length=100, default="Untitled Resume")
    template = models.ForeignKey(ResumeTemplate, on_delete=models.SET_NULL, null=True, blank=True)
    theme_color = models.CharField(max_length=20, default="#2563eb")
    ats_score = models.IntegerField(default=0)
    completion_percentage = models.IntegerField(default=0)
    
    # Store everything as JSON for maximum flexibility (drag & drop reordering, dynamic sections)
    content = models.JSONField(default=dict)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.title}"
