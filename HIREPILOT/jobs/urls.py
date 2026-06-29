from django.urls import path
from . views import *

urlpatterns = [
    path('roadmap/', roadmap_view, name='roadmap'),
    path('available-jobs/', available_jobs, name='available_jobs'),
    path('save_jobs/', update_desired_role, name='save_jobs'),
    path('matches/', job_matches, name='job_matches'),
    path('referrals/', referrals, name='referrals'),
]
