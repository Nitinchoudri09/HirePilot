from django.urls import path
from . import views

urlpatterns = [
    # Job Seeker
    path('', views.referral_marketplace, name='referral_marketplace'),
    path('request/<int:employee_id>/', views.request_referral, name='request_referral'),
    path('track/', views.track_referrals, name='track_referrals'),

    # Employee
    path('employee/signup/', views.employee_signup, name='employee_signup'),
    path('employee/verify/', views.verify_work_email, name='verify_work_email'),
    path('employee/resend-otp/', views.resend_otp, name='resend_otp'),
    path('employee/dashboard/', views.employee_dashboard, name='employee_dashboard'),
    path('respond/<int:pk>/', views.respond_to_referral, name='respond_to_referral'),
    path('stage/<int:pk>/', views.update_referral_stage, name='update_referral_stage'),

    # Invite
    path('invite/<uuid:code>/', views.invite_via_link, name='invite_via_link'),

    # Chat
    path('chat/<int:referral_pk>/', views.chat_thread, name='chat_thread'),

    # Notifications
    path('notifications/', views.notifications_list, name='notifications_list'),
    path('notifications/<int:pk>/read/', views.mark_notification_read, name='mark_notification_read'),
    path('notifications/count/', views.unread_notification_count, name='unread_notification_count'),
]
