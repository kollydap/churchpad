from rest_framework import serializers
from .models import Plan, Subscriber, Subscription


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ["id", "name", "price", "description"]
        read_only_fields = ["id"]


class SubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscriber
        fields = ["id", "name", "email", "phone_number", "created_at"]
        read_only_fields = ["id", "created_at"]


class SubscriptionSerializer(serializers.ModelSerializer):
    subscriber = SubscriberSerializer(read_only=True)
    plan = PlanSerializer(read_only=True)

    class Meta:
        model = Subscription
        fields = [
            "id",
            "subscriber",
            "plan",
            "status",
            "start_date",
            "end_date",
            "created_at",
        ]
        read_only_fields = ["id", "start_date", "end_date", "created_at"]


class SubscriptionCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    email = serializers.EmailField()
    phone_number = serializers.CharField(max_length=20)
    plan_id = serializers.IntegerField()

    def validate_plan_id(self, value):
        try:
            Plan.objects.get(pk=value)
            return value
        except Plan.DoesNotExist:
            raise serializers.ValidationError("Selected plan does not exist")
