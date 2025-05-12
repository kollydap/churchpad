from django.contrib import admin
from .models import Plan, Subscriber, Subscription


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "stripe_price_id", "created_at")
    search_fields = ("name", "stripe_price_id")


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone_number", "stripe_customer_id", "created_at")
    search_fields = ("name", "email", "phone_number", "stripe_customer_id")


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "get_subscriber_name",
        "get_plan_name",
        "status",
        "start_date",
        "end_date",
    )
    list_filter = ("status", "start_date")
    search_fields = (
        "subscriber__name",
        "subscriber__email",
        "plan__name",
        "stripe_subscription_id",
    )

    def get_subscriber_name(self, obj):
        return obj.subscriber.name

    get_subscriber_name.short_description = "Subscriber"

    def get_plan_name(self, obj):
        return obj.plan.name

    get_plan_name.short_description = "Plan"
