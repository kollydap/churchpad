from django.test import TestCase
from django.utils import timezone
from subscriptions.models import Plan, Subscriber, Subscription

class ModelTests(TestCase):
    def setUp(self):
        # Create test data
        self.plan = Plan.objects.create(
            name="Basic Plan",
            stripe_price_id="price_test123",
            price=9.99,
            description="Basic Streaming Plan"
        )
        
        self.subscriber = Subscriber.objects.create(
            name="Test User",
            email="test@example.com",
            phone_number="+15551234567",
            stripe_customer_id="cus_test123"
        )
        
        self.subscription = Subscription.objects.create(
            subscriber=self.subscriber,
            plan=self.plan,
            status='active',
            stripe_subscription_id="sub_test123",
            start_date=timezone.now()
        )

    def test_plan_creation(self):
        """Test that Plan model works correctly"""
        self.assertEqual(self.plan.name, "Basic Plan")
        self.assertEqual(self.plan.stripe_price_id, "price_test123")
        self.assertEqual(float(self.plan.price), 9.99)
        self.assertEqual(str(self.plan), "Basic Plan ($9.99)")

    def test_subscriber_creation(self):
        """Test that Subscriber model works correctly"""
        self.assertEqual(self.subscriber.name, "Test User")
        self.assertEqual(self.subscriber.email, "test@example.com")
        self.assertEqual(self.subscriber.phone_number, "+15551234567")
        self.assertEqual(str(self.subscriber), "Test User (test@example.com)")

    def test_subscription_creation(self):
        """Test that Subscription model works correctly"""
        self.assertEqual(self.subscription.subscriber, self.subscriber)
        self.assertEqual(self.subscription.plan, self.plan)
        self.assertEqual(self.subscription.status, 'active')
        self.assertEqual(self.subscription.stripe_subscription_id, "sub_test123")
        self.assertTrue(self.subscription.is_active)
        self.assertIn("Test User's Basic Plan subscription", str(self.subscription))