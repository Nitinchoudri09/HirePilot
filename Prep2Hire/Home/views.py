from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login
from django.views.generic import TemplateView
from django.contrib.auth import logout

class HomeView(TemplateView):
    def get(self, request):
        return render(request, 'index.html')

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)          # auto-login after signup
            return redirect('dashboard')        # go straight to dashboard
    else:
        form = UserCreationForm()
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