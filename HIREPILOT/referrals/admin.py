from django.contrib import admin
from .models import EmployeeProfile, CompanyInvite, ReferralRequest, ReferralNotification, ChatMessage

@admin.register(EmployeeProfile)
class EmployeeProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'company', 'job_title', 'work_email', 'is_verified', 'created_at']
    list_filter = ['is_verified', 'company']
    search_fields = ['user__username', 'company', 'work_email']

@admin.register(CompanyInvite)
class CompanyInviteAdmin(admin.ModelAdmin):
    list_display = ['company_name', 'email_domain', 'created_by', 'used_count', 'created_at']

@admin.register(ReferralRequest)
class ReferralRequestAdmin(admin.ModelAdmin):
    list_display = ['seeker', 'employee', 'status', 'stage', 'created_at']
    list_filter = ['status', 'stage']

@admin.register(ReferralNotification)
class ReferralNotificationAdmin(admin.ModelAdmin):
    list_display = ['recipient', 'notification_type', 'is_read', 'created_at']

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['referral_request', 'sender', 'sent_at']
