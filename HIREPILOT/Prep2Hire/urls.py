from django.contrib import admin
from django.urls import include
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Home.urls')),
    path('jobs/', include('jobs.urls')),
    path('skill-development/', include('skill_development.urls')),
    path('resume-analyzer/', include('resume_analyzer.urls')),
    path("coding/", include("judge.urls")),
    path('resumes/', include('resume_builder.urls')),
    path('referrals/', include('referrals.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.contrib.auth import views as auth_views

urlpatterns += [
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='accounts/password_reset.html',
             email_template_name='emails/password_reset_email.html',
             html_email_template_name='emails/password_reset_email.html',
             subject_template_name='emails/password_reset_subject.txt',
             success_url='/password-reset/done/'
         ), name='password_reset'),

    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='accounts/password_reset_done.html'
         ), name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='accounts/password_reset_confirm.html',
             success_url='/password-reset-complete/'
         ), name='password_reset_confirm'),

    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='accounts/password_reset_complete.html'
         ), name='password_reset_complete'),
]

from Home.views import verify_email_view, verification_sent_view

urlpatterns += [
    path('verify-email/<str:token>/', verify_email_view, name='verify_email'),
    path('verification-sent/', verification_sent_view, name='verification_sent'),
]
