from django.urls import path
from . import views

urlpatterns = [
    path('',                  views.analyze_resume,       name='analyze_resume'),
    path('pricing/',          views.pricing_page,         name='pricing_page'),
    path('subscribe/',        views.create_razorpay_order, name='create_razorpay_order'),
    path('payment/callback/', views.payment_callback,     name='payment_callback'),
    path('subscription/',     views.subscription_dashboard, name='subscription_dashboard'),
]
