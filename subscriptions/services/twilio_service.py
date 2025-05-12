from twilio.rest import Client
from django.conf import settings


class TwilioService:
    def __init__(self):
        self.client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        self.from_number = settings.TWILIO_PHONE_NUMBER

    def send_welcome_message(self, subscriber_name, phone_number):
        """
        Send a welcome SMS message to a new subscriber

        Args:
            subscriber_name (str): Name of the subscriber
            phone_number (str): Subscriber's phone number

        Returns:
            obj: Twilio message object
        """
        try:
            message = self.client.messages.create(
                body=f"Hi {subscriber_name}, thanks for subscribing to our livestream service on ChurchPad!",
                from_=self.from_number,
                to=phone_number,
            )
            return message
        except Exception as e:
            # Log the error and re-raise
            print(f"Twilio error: {str(e)}")
            raise
