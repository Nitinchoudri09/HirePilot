from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    desired_role = models.CharField(max_length=100)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)


class Job(models.Model):
    job_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    location = models.CharField(max_length=255, blank=True)
    description = models.TextField()
    url = models.URLField()
    date_posted = models.DateTimeField()

    def __str__(self):
        return self.name

class JobMatch(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="matches")
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="matches")
    eligibility_score = models.FloatField(default=0.0)
    matched_skills = models.JSONField(default=list, blank=True)
    missing_skills = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'job')

    def __str__(self):
        return f"{self.user.username} - {self.job.name} ({self.eligibility_score}%)"



