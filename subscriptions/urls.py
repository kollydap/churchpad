from django.urls import path
from . import views

urlpatterns = [
    # Plan endpoints
    path("plans/", views.get_plans, name="plan-list"),
    path("plans/<int:pk>/", views.get_plan, name="plan-detail"),
    # Subscription endpoints
    path("subscriptions/", views.get_subscriptions, name="subscription-list"),
    path("subscriptions/<int:pk>/", views.get_subscription, name="subscription-detail"),
    # Main API endpoints as per requirements
    path("subscribe/", views.create_subscription, name="subscribe"),
    path("unsubscribe/<int:pk>/", views.cancel_subscription, name="unsubscribe"),
    # Webhook endpoint
    path("webhook/", views.stripe_webhook, name="webhook"),
]
