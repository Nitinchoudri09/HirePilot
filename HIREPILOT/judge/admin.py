from django.contrib import admin
from .models import Problem, TestCase, Submission

class TestCaseInline(admin.TabularInline):
    model = TestCase
    extra = 1

@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = ('title','slug','created_at')
    inlines = [TestCaseInline]

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('id','problem','user','status','created_at')
    readonly_fields = ('details','created_at','runtime')
