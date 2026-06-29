from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Resume, ResumeTemplate, UserSubscription

@login_required
def dashboard(request):
    resumes = request.user.resumes.all().order_by('-updated_at')
    templates = ResumeTemplate.objects.all()
    
    context = {
        'resumes': resumes,
        'templates': templates,
    }
    return render(request, 'resume_builder/dashboard.html', context)

@login_required
def subscription(request):
    sub, created = UserSubscription.objects.get_or_create(user=request.user)
    return render(request, 'resume_builder/subscription.html', {'sub': sub})

@login_required
def builder(request, resume_id=None):
    if resume_id:
        resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    else:
        # Create a blank resume if creating new
        resume = Resume.objects.create(user=request.user)
        return redirect('resume_builder:builder', resume_id=resume.id)
        
    context = {
        'resume': resume,
        'templates': ResumeTemplate.objects.all()
    }
    return render(request, 'resume_builder/builder.html', context)

from django.http import JsonResponse
import json

@login_required
def update_resume(request, resume_id):
    if request.method == 'POST':
        resume = get_object_or_404(Resume, id=resume_id, user=request.user)
        try:
            data = json.loads(request.body)
            resume.title = data.get('title', resume.title)
            resume.content = data.get('content', resume.content)
            resume.ats_score = data.get('ats_score', resume.ats_score)
            resume.save()
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'invalid method'}, status=405)

@login_required
def ai_suggest_summary(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            role = data.get('role', 'Professional')
            # Mock AI response - in reality this would call OpenAI API
            ai_summary = f"Results-driven {role} with a proven track record of delivering high-quality solutions. Adept at leveraging modern technologies to optimize workflows, solve complex problems, and drive business growth in fast-paced environments."
            return JsonResponse({'status': 'success', 'summary': ai_summary})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

@login_required
def ai_suggest_keywords(request):
    if request.method == 'POST':
        try:
            # Mock ATS keywords based on role
            keywords = "Agile Methodology, Cross-functional Team Leadership, Data Analysis, Cloud Computing, Project Management, RESTful APIs"
            return JsonResponse({'status': 'success', 'keywords': keywords})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

@login_required
def delete_resume(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    if request.method == 'POST':
        resume.delete()
    return redirect('resume_builder:dashboard')
