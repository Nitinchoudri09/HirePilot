from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from . views import *

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('force-populate/', views.force_populate_db, name='force_populate_db'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('delete-account/', views.delete_account, name='delete_account'),
    # Google OAuth 2.0
    path('auth/google/', views.google_oauth_redirect, name='google_oauth_redirect'),
    path('auth/google/callback/', views.google_oauth_callback, name='google_oauth_callback'),
    path('career_recommendation/', views.career_quiz, name='career_recommendation'),
    path('carrer_recommendation/', views.career_quiz, name='carrer_recommendation_legacy'),
    path('connect/', views.post_list, name='post_list'),
    path('connect/new/', views.create_post, name='create_post'),
    path('connect/delete/<int:post_id>/', views.delete_post, name='delete_post'),
    path('connect/like/<int:post_id>/', views.like_post, name='like_post'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('change-password/', auth_views.PasswordChangeView.as_view(template_name='change_password.html', success_url='/dashboard/'), name='change_password'),
    
    # Password Reset URLs — using CustomPasswordResetView for robust SMTP error handling
    path('password-reset/', 
         views.CustomPasswordResetView.as_view(),
         name='password_reset'),
    path('password-reset/done/', 
         auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), 
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(
             template_name='password_reset_confirm.html',
             success_url='/password-reset-complete/'
         ), 
         name='password_reset_confirm'),
    path('password-reset-complete/', 
         auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), 
         name='password_reset_complete'),
]
