import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

class StripeService:
    @staticmethod
    def create_customer(name, email, phone):
        """
        Create a customer in Stripe
        
        Args:
            name (str): Customer name
            email (str): Customer email
            phone (str): Customer phone number
            
        Returns:
            str: Stripe customer ID
        """
        try:
            customer = stripe.Customer.create(
                name=name,
                email=email,
                phone=phone,
                description=f"ChurchPad subscriber: {name}"
            )
            return customer.id
        except stripe.error.StripeError as e:
            # Log the error and re-raise
            print(f"Stripe error: {str(e)}")
            raise
    
    @staticmethod
    def create_subscription(customer_id, price_id):
        """
        Create a subscription in Stripe
        
        Args:
            customer_id (str): Stripe customer ID
            price_id (str): Stripe price ID
            
        Returns:
            obj: Stripe subscription object
        """
        try:
            subscription = stripe.Subscription.create(
                customer=customer_id,
                items=[{"price": price_id}],
                expand=["latest_invoice.payment_intent"]
            )
            return subscription
        except stripe.error.StripeError as e:
            # Log the error and re-raise
            print(f"Stripe error: {str(e)}")
            raise
    
    @staticmethod
    def cancel_subscription(subscription_id):
        """
        Cancel a subscription in Stripe
        
        Args:
            subscription_id (str): Stripe subscription ID
            
        Returns:
            obj: Cancelled Stripe subscription object
        """
        try:
            subscription = stripe.Subscription.delete(subscription_id)
            return subscription
        except stripe.error.StripeError as e:
            # Log the error and re-raise
            print(f"Stripe error: {str(e)}")
            raise
            
    @staticmethod
    def retrieve_subscription(subscription_id):
        """
        Retrieve a subscription from Stripe
        
        Args:
            subscription_id (str): Stripe subscription ID
            
        Returns:
            obj: Stripe subscription object
        """
        try:
            subscription = stripe.Subscription.retrieve(subscription_id)
            return subscription
        except stripe.error.StripeError as e:
            # Log the error and re-raise
            print(f"Stripe error: {str(e)}")
            raise