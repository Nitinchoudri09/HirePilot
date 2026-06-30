import os
from django.shortcuts import render, redirect
from django.conf import settings
from .forms import DesiredRoleForm
from .models import Profile, Job
from django.contrib.auth.decorators import login_required

from django.core.mail import send_mail

def roadmap_view(request):
    roadmap_dir = os.path.join(settings.BASE_DIR, 'Home', 'static', 'assets', 'roadmaps')
    try:
        roadmap_files = os.listdir(roadmap_dir)
    except FileNotFoundError:
        roadmap_files = []
    
    context = {
        'roadmaps': [f'assets/roadmaps/{file}' for file in roadmap_files if file.endswith('.pdf')]
    }
    return render(request, 'roadmap.html', context)

def available_jobs(request):
    return render(request, 'jobs/available_jobs.html')

# views.py
@login_required
def update_desired_role(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    jobs = []

    if request.method == 'POST':
        form = DesiredRoleForm(request.POST, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            user_email = form.cleaned_data.get('email')
            desired_role = form.cleaned_data.get('desired_role')
            profile.save()

            # Filter jobs
            jobs = Job.objects.filter(name__icontains=desired_role)
            
            if jobs.exists():
                job_list = "\n".join([
                    f"Congratulations you have a job match! 😍 \nJob: {job.name} \nCompany: {job.company} \nLocation: {job.location}\nApply Now: {job.url}"
                    for job in jobs
                ])
                # Send email
                try:
                    send_mail(
                        subject=f'Hey! {request.user} 👋👋 You have a job match! ',
                        message=job_list,
                        from_email=settings.EMAIL_HOST_USER,
                        recipient_list=[user_email],
                        fail_silently=False,
                    )
                except Exception as e:
                    print("Email sending failed:", e)
            else:
                job_list = "No jobs matching your desired role at the moment."

    else:
        form = DesiredRoleForm(instance=profile)

    return render(request, 'update_desired_role.html', {'form': form, 'jobs': jobs})

@login_required
def job_matches(request):
    # Dummy integration for now, just fetch all jobs
    jobs = Job.objects.all()[:10]
    context = {'matches': jobs}
    return render(request, 'jobs/job_matches.html', context)

@login_required
def referrals(request):
    """Redirects to the new referrals marketplace."""
    return redirect('referral_marketplace')