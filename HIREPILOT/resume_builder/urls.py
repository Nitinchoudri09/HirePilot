from django.urls import path
from . import views

app_name = 'resume_builder'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('plans/', views.subscription, name='subscription'),
    path('builder/new/', views.builder, name='new_builder'),
    path('builder/<int:resume_id>/', views.builder, name='builder'),
    path('builder/<int:resume_id>/update/', views.update_resume, name='update_resume'),
    path('ai/summary/', views.ai_suggest_summary, name='ai_summary'),
    path('ai/keywords/', views.ai_suggest_keywords, name='ai_keywords'),
    path('delete/<int:resume_id>/', views.delete_resume, name='delete_resume'),
]
