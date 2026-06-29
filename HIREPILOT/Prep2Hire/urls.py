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
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
