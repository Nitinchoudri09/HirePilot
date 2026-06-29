from django.contrib import admin
from .models import ResumeTemplate, Resume, UserSubscription

@admin.register(UserSubscription)
class UserSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan', 'is_active')
    list_filter = ('plan', 'is_active')
    search_fields = ('user__username',)

@admin.register(ResumeTemplate)
class ResumeTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'template_id', 'category', 'required_plan', 'usage_count', 'is_active')
    list_filter = ('category', 'required_plan', 'is_active')
    search_fields = ('name', 'template_id')
    readonly_fields = ('usage_count',)

@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'template', 'ats_score', 'created_at')
    list_filter = ('template', 'created_at')
    search_fields = ('title', 'user__username')
