from django.contrib import admin
from .models import Quiz, Question, Option, QuizResult

class OptionInline(admin.TabularInline):
    model = Option
    extra = 4  # 4 options by default
    min_num = 1
    max_num = 4

class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1

class QuestionAdmin(admin.ModelAdmin):
    inlines = [OptionInline]
    list_display = ['text', 'quiz']

class QuizAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]
    list_display = ['title', 'description']

class QuizResultAdmin(admin.ModelAdmin):
    list_display = ['user', 'quiz', 'score', 'total', 'taken_at']
    list_filter = ['quiz', 'user']

# Registering all models
admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Option)
admin.site.register(QuizResult, QuizResultAdmin)
