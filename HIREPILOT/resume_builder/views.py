from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Resume, ResumeTemplate, UserSubscription, BuilderPayment
import json
import razorpay
import hmac
import hashlib
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseBadRequest

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
    return render(request, 'resume_builder/subscription.html', {
        'sub': sub,
        'razorpay_key': settings.RAZORPAY_KEY_ID
    })

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

def get_razorpay_client():
    return razorpay.Client(
        auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
    )

@login_required
def create_razorpay_order(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)

    try:
        data = json.loads(request.body)
        plan = data.get('plan')
        amount_paise = data.get('amount')
    except (json.JSONDecodeError, ValueError):
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    if plan not in dict(UserSubscription.PLAN_CHOICES).keys():
        return JsonResponse({'error': 'Invalid plan'}, status=400)

    client = get_razorpay_client()
    
    order_data = {
        'amount': amount_paise,
        'currency': 'INR',
        'receipt': f'builder_user_{request.user.id}_{plan}',
        'notes': {
            'user_id': str(request.user.id),
            'plan': plan,
        },
    }

    try:
        rz_order = client.order.create(data=order_data)
    except Exception as e:
        return JsonResponse({'error': f'Razorpay error: {str(e)}'}, status=502)

    BuilderPayment.objects.create(
        user=request.user,
        plan=plan,
        razorpay_order_id=rz_order['id'],
        amount=amount_paise / 100,
        currency='INR',
        status='created',
    )

    return JsonResponse({
        'order_id': rz_order['id'],
        'amount': amount_paise,
        'currency': 'INR',
        'plan_name': dict(UserSubscription.PLAN_CHOICES).get(plan),
    })

@csrf_exempt
@login_required
def payment_callback(request):
    if request.method != 'POST':
        return HttpResponseBadRequest()

    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    razorpay_order_id   = data.get('razorpay_order_id', '')
    razorpay_payment_id = data.get('razorpay_payment_id', '')
    razorpay_signature  = data.get('razorpay_signature', '')

    body = f"{razorpay_order_id}|{razorpay_payment_id}"
    expected_sig = hmac.new(
        settings.RAZORPAY_KEY_SECRET.encode(),
        body.encode(),
        hashlib.sha256,
    ).hexdigest()

    if not hmac.compare_digest(expected_sig, razorpay_signature):
        return JsonResponse({'ok': False, 'error': 'Invalid payment signature'}, status=400)

    try:
        payment = BuilderPayment.objects.get(razorpay_order_id=razorpay_order_id, user=request.user)
    except BuilderPayment.DoesNotExist:
        return JsonResponse({'ok': False, 'error': 'Payment record not found'}, status=404)

    payment.razorpay_payment_id = razorpay_payment_id
    payment.razorpay_signature  = razorpay_signature
    payment.status  = 'paid'
    payment.save()

    # Update subscription
    sub, created = UserSubscription.objects.get_or_create(user=request.user)
    sub.plan = payment.plan
    sub.save()

    return JsonResponse({'ok': True})
