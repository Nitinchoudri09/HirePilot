import os
from django.shortcuts import render, redirect
from django.conf import settings
from .forms import DesiredRoleForm
from .models import Profile, Job
from django.contrib.auth.decorators import login_required

from django.core.mail import send_mail

def roadmap_view(request):
    roadmap_dir = os.path.join(settings.MEDIA_ROOT, 'roadmaps')
    os.makedirs(roadmap_dir, exist_ok=True)  # ensure dir exists on fresh deploy
    try:
        roadmap_files = os.listdir(roadmap_dir)
    except OSError:
        roadmap_files = []
    context = {
        'roadmaps': [f'roadmaps/{file}' for file in roadmap_files if file.endswith('.pdf')]
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
    from .models import ReferralRequest
    
    if request.method == 'POST':
        job_id = request.POST.get('job_id')
        if job_id:
            job = Job.objects.get(id=job_id)
            from .ai_services import mock_generate_referral_message
            ai_msg = mock_generate_referral_message(request.user.username, job.name, ['Python', 'Django'])
            ReferralRequest.objects.create(
                candidate=request.user,
                job=job,
                message=ai_msg,
                ai_generated_message=ai_msg
            )
            return redirect('referrals')

    sent_referrals = ReferralRequest.objects.filter(candidate=request.user)
    # Also fetch some dummy jobs for the dropdown
    jobs = Job.objects.all()[:5]
    context = {'sent_referrals': sent_referrals, 'jobs': jobs}
    return render(request, 'jobs/referrals.html', context)