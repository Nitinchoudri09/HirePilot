from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from . views import *

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('about/', views.about_view, name='about'),
    path('force-populate/', views.force_populate_db, name='force_populate_db'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('delete-account/', views.delete_account, name='delete_account'),
    # Supabase Auth — called by JS frontend after Supabase OAuth completes
    path('auth/supabase/callback/', views.supabase_auth_callback, name='supabase_auth_callback'),
    path('career_recommendation/', views.career_quiz, name='career_recommendation'),
    path('carrer_recommendation/', views.career_quiz, name='carrer_recommendation_legacy'),
    path('connect/', views.post_list, name='post_list'),
    path('connect/new/', views.create_post, name='create_post'),
    path('connect/delete/<int:post_id>/', views.delete_post, name='delete_post'),
    path('connect/like/<int:post_id>/', views.like_post, name='like_post'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('change-password/', auth_views.PasswordChangeView.as_view(template_name='change_password.html', success_url='/dashboard/'), name='change_password'),
    
    path('profile/', views.profile_settings_view, name='profile_settings'),
    path('profile/add-task/', views.add_task, name='add_task'),
    path('profile/toggle-task/<int:task_id>/', views.toggle_task, name='toggle_task'),
    path('profile/delete-task/<int:task_id>/', views.delete_task, name='delete_task'),
]
