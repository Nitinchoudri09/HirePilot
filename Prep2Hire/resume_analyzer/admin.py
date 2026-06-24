from django.contrib import admin
from .models import SubscriptionPlan, UserSubscription, Payment, ResumeAnalysisHistory


@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display  = ('name', 'plan_type', 'price', 'credits', 'validity_days', 'is_active')
    list_editable = ('price', 'credits', 'is_active')
    list_filter   = ('is_active', 'plan_type')
    search_fields = ('name',)


@admin.register(UserSubscription)
class UserSubscriptionAdmin(admin.ModelAdmin):
    list_display  = ('user', 'plan', 'credits_remaining', 'status', 'expiry_date', 'updated_at')
    list_filter   = ('status', 'plan')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('start_date', 'updated_at')
    ordering = ('-updated_at',)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'plan')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display  = ('user', 'plan', 'amount', 'currency', 'status', 'razorpay_order_id', 'created_at', 'paid_at')
    list_filter   = ('status', 'currency', 'plan')
    search_fields = ('user__username', 'user__email', 'razorpay_order_id', 'razorpay_payment_id')
    readonly_fields = ('created_at', 'paid_at', 'razorpay_order_id', 'razorpay_payment_id', 'razorpay_signature')
    ordering = ('-created_at',)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'plan')


@admin.register(ResumeAnalysisHistory)
class ResumeAnalysisHistoryAdmin(admin.ModelAdmin):
    list_display  = ('user', 'job_title', 'ats_score', 'created_at')
    list_filter   = ('created_at',)
    search_fields = ('user__username', 'job_title')
    readonly_fields = ('created_at', 'missing_keywords', 'suggestions')
    ordering = ('-created_at',)
