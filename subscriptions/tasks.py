from celery import shared_task
from twilio.rest import Client
import os

@shared_task
def send_welcome_sms(name, phone_number):
    account_sid = os.getenv('TWILIO_SID')
    auth_token = os.getenv('TWILIO_AUTH_TOKEN')
    from_number = os.getenv('TWILIO_PHONE_NUMBER')

    client = Client(account_sid, auth_token)
    message = f"Hi {name}, thanks for subscribing to our livestream service on ChurchPad!"
    client.messages.create(body=message, from_=from_number, to=phone_number)
