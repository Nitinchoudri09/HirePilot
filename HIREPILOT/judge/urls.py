from django.urls import path
from . import views

app_name = "judge"

urlpatterns = [
    path("", views.problem_list, name="problem_list"),
    path("problem/<slug:slug>/", views.problem_detail, name="problem_detail"),
    path("problem/<slug:slug>/submit/", views.submit_solution, name="submit_solution"),
    path("problem/<slug:slug>/run/", views.run_code, name="run_code"),
    path("submission/<int:submission_id>/", views.submission_result, name="submission_result"),
]
