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
from Home.views import custom_password_reset_view

urlpatterns += [
    path('password-reset/', custom_password_reset_view, name='password_reset'),

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
