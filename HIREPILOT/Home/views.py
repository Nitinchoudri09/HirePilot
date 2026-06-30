from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.contrib import messages
from django.core.mail import BadHeaderError
from smtplib import SMTPException
import socket
import subprocess
import logging
from django.contrib.auth import login as auth_login

logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────────────────────────────────────
# Supabase Auth — Token verification imports
# ─────────────────────────────────────────────────────────────────────────────
import json
import requests as http_requests
from django.conf import settings
from django.contrib.auth.models import User
from django.http import JsonResponse
import os


# ─────────────────────────────────────────────────────────────────────────────
# Supabase Auth — Token verification + Django session creation
# Called via POST from the frontend JS after Supabase completes the OAuth flow.
# ─────────────────────────────────────────────────────────────────────────────
@csrf_exempt
def supabase_auth_callback(request):
    """
    Receives a POST from the Supabase JS SDK after a successful OAuth login.
    Body JSON: { access_token: "...", email: "...", full_name: "..." }

    Steps:
      1. Verify the access token with Supabase's /auth/v1/user endpoint.
      2. Get-or-create a Django User from the verified email.
      3. Log the user in (create Django session).
      4. Return JSON { ok: true, redirect: "/dashboard/" }.

    All exceptions are caught at the top level so the response is always
    JSON — never an HTML 500 page.
    """
    # ─ Guard: POST only ──────────────────────────────────────────────────────
    if request.method != 'POST':
        return JsonResponse({'ok': False, 'error': 'POST required'}, status=405)

    try:
        # ─ Parse body ────────────────────────────────────────────────────────
        try:
            body = json.loads(request.body)
        except (json.JSONDecodeError, ValueError):
            return JsonResponse({'ok': False, 'error': 'Invalid JSON'}, status=400)

        access_token = body.get('access_token', '').strip()
        if not access_token:
            return JsonResponse({'ok': False, 'error': 'Missing access_token'}, status=400)

        # ─ Validate Supabase credentials are configured ──────────────────────
        supabase_url = getattr(settings, 'SUPABASE_URL', '').strip()
        supabase_key = getattr(settings, 'SUPABASE_KEY', '').strip()

        print("SUPABASE_URL loaded:", bool(supabase_url))
        print("SUPABASE_KEY loaded:", bool(supabase_key))
        print("access token received:", bool(access_token))

        if not supabase_url or not supabase_key:
            logger.error('SUPABASE_URL or SUPABASE_KEY is not configured.')
            return JsonResponse(
                {'ok': False, 'error': 'Server misconfiguration: Supabase credentials missing'},
                status=500,
            )

        # ─ Verify token with Supabase REST API ───────────────────────────────
        headers = {
            'Authorization': f'Bearer {access_token}',
            'apikey': supabase_key,
        }
        try:
            resp = http_requests.get(
                f'{supabase_url}/auth/v1/user',
                headers=headers,
                timeout=10,
            )
            if resp.status_code != 200:
                logger.warning(
                    'Supabase token verification failed. Status: %s  Body: %s',
                    resp.status_code, resp.text[:200],
                )
                return JsonResponse(
                    {'ok': False, 'error': 'Supabase token verification failed'},
                    status=401,
                )
            user_data = resp.json()
        except http_requests.RequestException as exc:
            logger.error('Network error reaching Supabase: %s', exc)
            return JsonResponse({'ok': False, 'error': f'Network error: {exc}'}, status=502)

        # ─ Extract user info ─────────────────────────────────────────────────
        email = (user_data.get('email') or body.get('email', '')).lower().strip()
        if not email:
            return JsonResponse({'ok': False, 'error': 'No email in Supabase response'}, status=400)

        user_meta = user_data.get('user_metadata', {})
        full_name  = user_meta.get('full_name') or user_meta.get('name') or body.get('full_name', '')
        name_parts = full_name.split(' ', 1) if full_name else []
        first_name = name_parts[0] if name_parts else ''
        last_name  = name_parts[1] if len(name_parts) > 1 else ''

        # ─ Safe email lookup ─────────────────────────────────────────────────
        # IMPORTANT: Django's default User model does NOT enforce email uniqueness.
        # get_or_create(email=...) raises MultipleObjectsReturned if duplicates exist.
        # We use filter().first() instead and create only when no match is found.
        user = User.objects.filter(email=email).first()

        if user is None:
            # Generate a unique username from the email local-part
            base_username = email.split('@')[0][:30]  # Django max_length=150, but 30 is safe
            username = base_username
            counter = 1
            while User.objects.filter(username=username).exists():
                username = f'{base_username}{counter}'[:30]
                counter += 1

            user = User(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
            )
            user.set_unusable_password()  # Supabase/Google users don't need a local password
            user.save()
            logger.info('Created new Django user: %s (%s)', username, email)
        else:
            # Update name fields if they are currently blank
            changed = False
            if not user.first_name and first_name:
                user.first_name = first_name
                changed = True
            if not user.last_name and last_name:
                user.last_name = last_name
                changed = True
            if changed:
                user.save(update_fields=['first_name', 'last_name'])

        # ─ Log in — create Django session ────────────────────────────────────
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        auth_login(request, user)
        logger.info('Logged in user via Supabase OAuth: %s', user.username)

        return JsonResponse({'ok': True, 'redirect': '/dashboard/'})

    except Exception as exc:
        # Top-level safety net — ensures we ALWAYS return JSON, never an HTML 500 page
        logger.exception('Unexpected error in supabase_auth_callback: %s', exc)
        return JsonResponse(
            {'ok': False, 'error': 'An unexpected server error occurred. Please try again.'},
            status=500,
        )





# ─────────────────────────────────────────────────────────────────────────────
# Custom Forgot Password View — handles SMTP errors, invalid email, and
# network issues gracefully instead of raising a 500 error.
# ─────────────────────────────────────────────────────────────────────────────
class CustomPasswordResetView(PasswordResetView):
    """Extends Django's built-in PasswordResetView with robust error handling."""
    template_name = 'password_reset_form.html'
    email_template_name = 'registration/password_reset_email.html'
    subject_template_name = 'registration/password_reset_subject.txt'
    success_url = '/password-reset/done/'

    def form_valid(self, form):
        """Attempt to send the reset email; catch SMTP/network failures."""
        email = form.cleaned_data.get('email', '').strip().lower()
        try:
            response = super().form_valid(form)
            return response
        except BadHeaderError:
            messages.error(
                self.request,
                'Invalid email header detected. Please use a valid email address.'
            )
            return self.form_invalid(form)
        except SMTPException as e:
            messages.error(
                self.request,
                'We could not send the email due to a mail server issue. '
                'Please try again later or contact support.'
            )
            return self.form_invalid(form)
        except socket.gaierror:
            messages.error(
                self.request,
                'Network error: Unable to reach the mail server. '
                'Check your internet connection and try again.'
            )
            return self.form_invalid(form)
        except Exception:
            messages.error(
                self.request,
                'An unexpected error occurred. Please try again or contact support.'
            )
            return self.form_invalid(form)

def force_populate_db(request):
    try:
        out1 = subprocess.check_output(['python', 'populate_quizzes.py'], stderr=subprocess.STDOUT)
        out2 = subprocess.check_output(['python', 'populate_problems.py'], stderr=subprocess.STDOUT)
        out3 = subprocess.check_output(['python', 'populate_career.py'], stderr=subprocess.STDOUT)
        return HttpResponse(f"<pre>Quizzes:\n{out1.decode('utf-8')}\nProblems:\n{out2.decode('utf-8')}\nCareers:\n{out3.decode('utf-8')}</pre>")
    except subprocess.CalledProcessError as e:
        return HttpResponse(f"<pre>Error:\n{e.output.decode('utf-8')}</pre>")

class HomeView(TemplateView):
    def get(self, request):
        return render(request, 'index.html')

def about_view(request):
    return render(request, 'about.html')

from .forms import SignupForm

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user, backend='Home.backends.EmailOrUsernameModelBackend')          # auto-login after signup
            return redirect('dashboard')        # go straight to dashboard
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

def custom_logout(request):
    logout(request)
    return redirect('/')

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt

@login_required
@csrf_exempt  # Optional if you want GET request (not recommended for delete)
def delete_account(request):
    if request.method == "POST":
        user = request.user
        logout(request)         # Logs out the user
        user.delete()           # Deletes the user from DB
        return redirect('/')    # Redirect to homepage (or show a message)
    else:
        return redirect('/') 
    

from .models import Question, Option, CareerSuggestion

def career_quiz(request):
    questions = Question.objects.all()

    if request.method == 'POST':
        scores = {}
        for q in questions:
            selected = request.POST.get(f'question_{q.id}')
            if selected:
                option = Option.objects.get(id=selected)
                for career, val in option.score_map.items():
                    scores[career] = scores.get(career, 0) + val

        # Find top scoring career
        if not scores:
            return render(request, 'career_quiz.html', {'questions': questions, 'error': 'Please select at least one option.'})
            
        suggested_career = max(scores, key=scores.get)
        suggestion = CareerSuggestion.objects.get(career=suggested_career)
        return render(request, 'carreer_result.html', {'suggestion': suggestion})

    return render(request, 'career_quiz.html', {'questions': questions})

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post, Like
from .forms import PostForm

from .models import Post, Like

@login_required
def post_list(request):
    posts = Post.objects.all().order_by('-created_at')

    for post in posts:
        post.has_liked = post.likes.filter(user=request.user).exists()

    return render(request, 'connect/post_list.html', {'posts': posts})

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.user = request.user
            new_post.save()
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'connect/post_form.html', {'form': form})

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.user == request.user:
        post.delete()
    return redirect('post_list')

from django.http import JsonResponse

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    liked = False

    like, created = Like.objects.get_or_create(post=post, user=request.user)
    if not created:
        like.delete()
    else:
        liked = True

    return JsonResponse({
        'liked': liked,
        'total_likes': post.likes.count()
    })

@login_required
def dashboard(request):
    from judge.models import Submission, Problem
    from skill_development.models import QuizResult, Quiz
    from django.utils import timezone
    from datetime import timedelta

    user = request.user
    now = timezone.now()
    one_week_ago = now - timedelta(days=7)

    # --- Coding Stats ---
    all_submissions = Submission.objects.filter(user=user)
    total_submissions = all_submissions.count()
    problems_solved = all_submissions.filter(status='AC').values('problem').distinct().count()
    problems_solved_this_week = all_submissions.filter(
        status='AC', created_at__gte=one_week_ago
    ).values('problem').distinct().count()

    # --- Quiz Stats ---
    all_quiz_results = QuizResult.objects.filter(user=user)
    quizzes_taken = all_quiz_results.values('quiz').distinct().count()
    quizzes_this_week = all_quiz_results.filter(
        taken_at__gte=one_week_ago
    ).values('quiz').distinct().count()

    # Average quiz score as percentage
    avg_quiz_score = 0
    if all_quiz_results.exists():
        total_score = sum(r.score for r in all_quiz_results)
        total_possible = sum(r.total for r in all_quiz_results)
        if total_possible > 0:
            avg_quiz_score = round((total_score / total_possible) * 100)

    # --- Posts Stats ---
    user_posts = Post.objects.filter(user=user)
    total_posts = user_posts.count()
    posts_this_week = user_posts.filter(created_at__gte=one_week_ago).count()

    # --- Total Likes Received ---
    total_likes_received = Like.objects.filter(post__user=user).count()

    # --- Recent Activity (last 10 events combined) ---
    recent_activity = []

    # Recent quiz results
    for qr in all_quiz_results.select_related('quiz').order_by('-taken_at')[:5]:
        pct = round((qr.score / qr.total) * 100) if qr.total > 0 else 0
        recent_activity.append({
            'icon': 'bx-trophy',
            'icon_class': 'icon-purple',
            'title': 'Quiz Completed',
            'desc': f'{qr.quiz.title} — {qr.score}/{qr.total} ({pct}%)',
            'time': qr.taken_at,
        })

    # Recent submissions
    for sub in all_submissions.select_related('problem').order_by('-created_at')[:5]:
        status_map = {
            'AC': 'Accepted ✅', 'WA': 'Wrong Answer ❌',
            'TLE': 'Time Limit ⏰', 'RE': 'Runtime Error 💥',
        }
        verdict = status_map.get(sub.status, sub.status)
        recent_activity.append({
            'icon': 'bx-code-alt',
            'icon_class': 'icon-blue',
            'title': f'Code Submission — {verdict}',
            'desc': sub.problem.title,
            'time': sub.created_at,
        })

    # Recent posts
    for post in user_posts.order_by('-created_at')[:5]:
        recent_activity.append({
            'icon': 'bx-message-square-dots',
            'icon_class': 'icon-green',
            'title': 'New Post Created',
            'desc': post.content[:80] + ('...' if len(post.content) > 80 else ''),
            'time': post.created_at,
        })

    # Sort all activity by time descending, take top 8
    recent_activity.sort(key=lambda x: x['time'], reverse=True)
    recent_activity = recent_activity[:8]

    # Calculate human-readable time-ago for each activity
    for activity in recent_activity:
        diff = now - activity['time']
        seconds = diff.total_seconds()
        if seconds < 60:
            activity['time_ago'] = 'Just now'
        elif seconds < 3600:
            mins = int(seconds // 60)
            activity['time_ago'] = f'{mins}m ago'
        elif seconds < 86400:
            hours = int(seconds // 3600)
            activity['time_ago'] = f'{hours}h ago'
        else:
            days = int(seconds // 86400)
            activity['time_ago'] = f'{days}d ago'

    context = {
        'problems_solved': problems_solved,
        'problems_solved_this_week': problems_solved_this_week,
        'total_submissions': total_submissions,
        'quizzes_taken': quizzes_taken,
        'quizzes_this_week': quizzes_this_week,
        'avg_quiz_score': avg_quiz_score,
        'total_posts': total_posts,
        'posts_this_week': posts_this_week,
        'total_likes_received': total_likes_received,
        'recent_activity': recent_activity,
    }
    return render(request, 'dashboard.html', context)

from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm, ProfileUpdateForm, UserTaskForm
from jobs.models import Profile

@login_required
def profile_settings_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile_settings')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=profile)

    tasks = request.user.tasks.all().order_by('-created_at')
    task_form = UserTaskForm()

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'tasks': tasks,
        'task_form': task_form
    }
    return render(request, 'profile_settings.html', context)

@login_required
def add_task(request):
    if request.method == 'POST':
        form = UserTaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
    return redirect('profile_settings')

@login_required
def toggle_task(request, task_id):
    from .models import UserTask
    task = get_object_or_404(UserTask, id=task_id, user=request.user)
    task.is_completed = not task.is_completed
    task.save()
    return redirect('profile_settings')

@login_required
def delete_task(request, task_id):
    from .models import UserTask
    task = get_object_or_404(UserTask, id=task_id, user=request.user)
    task.delete()
    return redirect('profile_settings')