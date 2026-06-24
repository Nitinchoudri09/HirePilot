import json
import hmac
import hashlib
import razorpay

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseBadRequest
from django.conf import settings
from django.utils import timezone
from django.contrib import messages
from datetime import timedelta

from .forms import ResumeForm
from .utils import extract_text
from .ai import calculate_similarity, missing_keywords, generate_suggestions
from .models import SubscriptionPlan, UserSubscription, Payment, ResumeAnalysisHistory
from .utils_email import send_payment_confirmation, send_low_credits_warning


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

def get_razorpay_client():
    return razorpay.Client(
        auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
    )


def get_or_create_subscription(user):
    """Return the user's subscription, creating a blank one if missing."""
    sub, _ = UserSubscription.objects.get_or_create(
        user=user,
        defaults={'credits_remaining': 0, 'status': 'active'},
    )
    return sub


# ─────────────────────────────────────────────────────────────────────────────
# Pricing Page
# ─────────────────────────────────────────────────────────────────────────────

def pricing_page(request):
    plans = SubscriptionPlan.objects.filter(is_active=True).order_by('price')
    subscription = None
    if request.user.is_authenticated:
        subscription = get_or_create_subscription(request.user)
    return render(request, 'pricing.html', {
        'plans': plans,
        'subscription': subscription,
        'razorpay_key': settings.RAZORPAY_KEY_ID,
    })


# ─────────────────────────────────────────────────────────────────────────────
# Create Razorpay Order (AJAX POST)
# ─────────────────────────────────────────────────────────────────────────────

@login_required
def create_razorpay_order(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)

    try:
        data = json.loads(request.body)
        plan_id = data.get('plan_id')
    except (json.JSONDecodeError, ValueError):
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    plan = get_object_or_404(SubscriptionPlan, id=plan_id, is_active=True)

    client = get_razorpay_client()
    amount_paise = int(plan.price * 100)  # Razorpay uses paise

    order_data = {
        'amount': amount_paise,
        'currency': 'INR',
        'receipt': f'order_user_{request.user.id}_plan_{plan.id}',
        'notes': {
            'user_id': str(request.user.id),
            'plan_id': str(plan.id),
            'plan_name': plan.name,
        },
    }

    try:
        rz_order = client.order.create(data=order_data)
    except Exception as e:
        return JsonResponse({'error': f'Razorpay error: {str(e)}'}, status=502)

    # Save pending payment record
    Payment.objects.create(
        user=request.user,
        plan=plan,
        razorpay_order_id=rz_order['id'],
        amount=plan.price,
        currency='INR',
        status='created',
    )

    return JsonResponse({
        'order_id': rz_order['id'],
        'amount': amount_paise,
        'currency': 'INR',
        'plan_name': plan.name,
        'user_email': request.user.email,
        'user_name': request.user.get_full_name() or request.user.username,
    })


# ─────────────────────────────────────────────────────────────────────────────
# Payment Callback — verify signature, activate subscription
# ─────────────────────────────────────────────────────────────────────────────

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

    # Verify signature
    body = f"{razorpay_order_id}|{razorpay_payment_id}"
    expected_sig = hmac.new(
        settings.RAZORPAY_KEY_SECRET.encode(),
        body.encode(),
        hashlib.sha256,
    ).hexdigest()

    if not hmac.compare_digest(expected_sig, razorpay_signature):
        return JsonResponse({'ok': False, 'error': 'Invalid payment signature'}, status=400)

    # Fetch & update payment record
    try:
        payment = Payment.objects.get(razorpay_order_id=razorpay_order_id, user=request.user)
    except Payment.DoesNotExist:
        return JsonResponse({'ok': False, 'error': 'Payment record not found'}, status=404)

    payment.razorpay_payment_id = razorpay_payment_id
    payment.razorpay_signature  = razorpay_signature
    payment.status  = 'paid'
    payment.paid_at = timezone.now()
    payment.save()

    # Activate / upgrade subscription
    plan = payment.plan
    sub  = get_or_create_subscription(request.user)
    sub.plan              = plan
    sub.credits_remaining = (sub.credits_remaining + plan.credits) if sub.is_valid and sub.plan == plan else plan.credits
    sub.expiry_date = timezone.now() + timedelta(days=plan.validity_days)
    sub.status      = 'active'
    sub.save()

    # Email confirmation
    send_payment_confirmation(request.user, plan, payment)

    return JsonResponse({'ok': True, 'redirect': '/resume-analyzer/subscription/'})


# ─────────────────────────────────────────────────────────────────────────────
# Subscription Dashboard
# ─────────────────────────────────────────────────────────────────────────────

@login_required
def subscription_dashboard(request):
    subscription = get_or_create_subscription(request.user)
    history      = ResumeAnalysisHistory.objects.filter(user=request.user)[:10]
    payments     = Payment.objects.filter(user=request.user, status='paid')[:5]
    plans        = SubscriptionPlan.objects.filter(is_active=True)

    return render(request, 'subscription_dashboard.html', {
        'subscription': subscription,
        'history':      history,
        'payments':     payments,
        'plans':        plans,
    })


# ─────────────────────────────────────────────────────────────────────────────
# Analyze Resume — with credit gating
# ─────────────────────────────────────────────────────────────────────────────

@login_required
def analyze_resume(request):
    subscription = get_or_create_subscription(request.user)
    score        = None
    suggestions  = []
    missing_words = []
    show_upgrade_popup = False

    if request.method == 'POST':
        # ── Credit gate ──────────────────────────────────────────────────
        if not subscription.is_valid or subscription.credits_remaining <= 0:
            show_upgrade_popup = True
            form = ResumeForm()
            return render(request, 'analyze.html', {
                'form': form,
                'subscription': subscription,
                'show_upgrade_popup': True,
            })

        form = ResumeForm(request.POST, request.FILES)
        if form.is_valid():
            resume_file = request.FILES['resume']
            job_desc    = form.cleaned_data['job_description']
            job_title   = form.cleaned_data.get('job_title', '')
            resume_text = extract_text(resume_file)

            score         = calculate_similarity(resume_text, job_desc)
            missing_words = missing_keywords(resume_text, job_desc)
            suggestions   = generate_suggestions(missing_words)

            # Deduct 1 credit
            subscription.credits_remaining = max(0, subscription.credits_remaining - 1)
            subscription.save(update_fields=['credits_remaining'])

            # Log to history
            ResumeAnalysisHistory.objects.create(
                user=request.user,
                job_title=job_title,
                ats_score=score,
                missing_keywords=missing_words[:20],
                suggestions=suggestions,
            )

            # Low credits warning email (send when exactly 1 remains)
            if subscription.credits_remaining == 1:
                send_low_credits_warning(request.user, 1)
    else:
        form = ResumeForm()

    return render(request, 'analyze.html', {
        'form':         form,
        'score':        score,
        'suggestions':  suggestions,
        'missing_words': missing_words,
        'subscription': subscription,
        'show_upgrade_popup': show_upgrade_popup,
    })
