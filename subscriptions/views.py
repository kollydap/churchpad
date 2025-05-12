from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.utils import timezone

from .models import Plan, Subscriber, Subscription
from .serializers import (
    PlanSerializer,
    SubscriberSerializer,
    SubscriptionSerializer,
    SubscriptionCreateSerializer,
)
from subscriptions.services.stripe_service import StripeService
from .tasks import send_welcome_sms


@api_view(["GET"])
def get_plans(request):
    """
    GET /plans/ - List all plans
    """
    plans = Plan.objects.all()
    serializer = PlanSerializer(plans, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def get_plan(request, pk):
    """
    GET /plans/{id}/ - Retrieve a specific plan
    """
    plan = get_object_or_404(Plan, pk=pk)
    serializer = PlanSerializer(plan)
    return Response(serializer.data)


@api_view(["GET"])
def get_subscriptions(request):
    """
    GET /subscriptions/ - List all active subscriptions
    """
    subscriptions = Subscription.objects.filter(status="active")
    serializer = SubscriptionSerializer(subscriptions, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def get_subscription(request, pk):
    """
    GET /subscriptions/{id}/ - Retrieve a specific subscription
    """
    subscription = get_object_or_404(Subscription, pk=pk)
    serializer = SubscriptionSerializer(subscription)
    return Response(serializer.data)


@api_view(["POST"])
@transaction.atomic
def create_subscription(request):
    """
    POST /subscribe/ - Create a new subscription
    """
    serializer = SubscriptionCreateSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    data = serializer.validated_data
    name = data["name"]
    email = data["email"]
    phone_number = data["phone_number"]
    plan_id = data["plan_id"]

    try:
        # Get or create subscriber
        try:
            subscriber = Subscriber.objects.get(email=email)
        except Subscriber.DoesNotExist:
            # Create Stripe customer
            stripe_customer_id = StripeService.create_customer(
                name, email, phone_number
            )

            # Create subscriber in database
            subscriber = Subscriber.objects.create(
                name=name,
                email=email,
                phone_number=phone_number,
                stripe_customer_id=stripe_customer_id,
            )

        # Get the plan
        plan = Plan.objects.get(pk=plan_id)

        # Create subscription in Stripe
        stripe_subscription = StripeService.create_subscription(
            subscriber.stripe_customer_id, plan.stripe_price_id
        )

        # Save subscription in database
        subscription = Subscription.objects.create(
            subscriber=subscriber,
            plan=plan,
            stripe_subscription_id=stripe_subscription.id,
            status="active",
            start_date=timezone.now(),
        )

        # Send welcome SMS asynchronously
        send_welcome_sms.delay(subscriber.name, subscriber.phone_number)

        # Return subscription details
        response_serializer = SubscriptionSerializer(subscription)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    except Plan.DoesNotExist:
        return Response(
            {"error": "The selected plan does not exist"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    except Exception as e:
        # Log the exception
        print(f"Error creating subscription: {str(e)}")
        return Response(
            {"error": "Failed to create subscription. Please try again."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["DELETE"])
@transaction.atomic
def cancel_subscription(request, pk):
    """
    DELETE /unsubscribe/{id}/ - Cancel a subscription
    """
    try:
        subscription = get_object_or_404(Subscription, pk=pk)

        if subscription.status != "active":
            return Response(
                {"error": "This subscription is not active"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Cancel subscription in Stripe
        StripeService.cancel_subscription(subscription.stripe_subscription_id)

        # Update subscription status in database
        subscription.status = "canceled"
        subscription.end_date = timezone.now()
        subscription.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

    except Exception as e:
        # Log the exception
        print(f"Error canceling subscription: {str(e)}")
        return Response(
            {"error": "Failed to cancel subscription. Please try again."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["POST"])
def stripe_webhook(request):
    """
    POST /webhook/ - Handle Stripe webhook events
    """
    # Simplified webhook implementation for the take-home test
    # In a real application, we would verify the signature and handle various event types

    try:
        event_type = request.data.get("type")
        event_data = request.data.get("data", {}).get("object", {})

        if event_type == "customer.subscription.deleted":
            subscription_id = event_data.get("id")
            subscription = Subscription.objects.filter(
                stripe_subscription_id=subscription_id
            ).first()

            if subscription:
                subscription.status = "canceled"
                subscription.end_date = timezone.now()
                subscription.save()

        return Response({"status": "success"})

    except Exception as e:
        # Log the exception
        print(f"Error processing webhook: {str(e)}")
        return Response(
            {"error": "Failed to process webhook"}, status=status.HTTP_400_BAD_REQUEST
        )
