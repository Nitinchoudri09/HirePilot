from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Problem(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class TestCase(models.Model):
    problem = models.ForeignKey(Problem, related_name='testcases', on_delete=models.CASCADE)
    input_data = models.TextField()    # raw input
    expected_output = models.TextField()
    is_hidden = models.BooleanField(default=False)  # hide from user (optional)

    def __str__(self):
        return f"TC for {self.problem.title} ({'hidden' if self.is_hidden else 'public'})"

class Submission(models.Model):
    STATUS_CHOICES = [
        ('PENDING','Pending'),
        ('RUNNING','Running'),
        ('AC','Accepted'),
        ('WA','Wrong Answer'),
        ('RE','Runtime Error'),
        ('TLE','Time Limit Exceeded'),
        ('ERR','Error'),
    ]

    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    problem = models.ForeignKey(Problem, related_name='submissions', on_delete=models.CASCADE)
    code = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    details = models.TextField(blank=True)  # store per-testcase results JSON or text
    runtime = models.FloatField(null=True, blank=True)  # total runtime seconds

    def __str__(self):
        return f"Submission {self.id} - {self.problem.title} - {self.status}"
