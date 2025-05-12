# Subscription Service API

This is a RESTful API built with Django and Django REST Framework that allows you to manage subscription plans and subscriptions for your service.

## Features

- Browse available subscription plans
- Create new subscriptions with Stripe integration
- Cancel existing subscriptions
- Automatic handling of Stripe webhooks
- SMS notifications for subscription events

## Installation

### Prerequisites

- Python 3.8+
- Django 3.2+
- Django REST Framework
- Stripe account
- Celery (for asynchronous tasks)

### Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/subscription-service-api.git
   cd subscription-service-api
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:

   ```bash
   cp .env.example .env
   ```

   Edit the `.env` file to include your Stripe API keys and other configuration.

5. Run migrations:

   ```bash
   python manage.py migrate
   ```

6. Start the development server:

   ```bash
   python manage.py runserver
   ```

7. Start Celery worker (in a separate terminal):
   ```bash
   celery -A project_name worker --loglevel=info
   ```

## API Endpoints

### Plans

| Method | Endpoint       | Description                    |
| ------ | -------------- | ------------------------------ |
| GET    | `/plans/`      | List all available plans       |
| GET    | `/plans/{id}/` | Get details of a specific plan |

### Subscriptions

| Method | Endpoint               | Description                            |
| ------ | ---------------------- | -------------------------------------- |
| GET    | `/subscriptions/`      | List all active subscriptions          |
| GET    | `/subscriptions/{id}/` | Get details of a specific subscription |
| POST   | `/subscribe/`          | Create a new subscription              |
| DELETE | `/unsubscribe/{id}/`   | Cancel an existing subscription        |

### Webhooks

| Method | Endpoint    | Description                        |
| ------ | ----------- | ---------------------------------- |
| POST   | `/webhook/` | Endpoint for Stripe webhook events |

## Usage Examples

### List all plans

```bash
curl -X GET http://localhost:8000/plans/
```

Response:

```json
[
  {
    "id": 1,
    "name": "Basic Plan",
    "description": "Basic features for individuals",
    "price": "9.99",
    "billing_interval": "month",
    "stripe_price_id": "price_1234567890"
  },
  {
    "id": 2,
    "name": "Premium Plan",
    "description": "Advanced features for professionals",
    "price": "19.99",
    "billing_interval": "month",
    "stripe_price_id": "price_0987654321"
  }
]
```

### Create a subscription

```bash
curl -X POST http://localhost:8000/subscribe/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "phone_number": "+1234567890",
    "plan_id": 1
  }'
```

Response:

```json
{
  "id": 1,
  "subscriber": {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "phone_number": "+1234567890"
  },
  "plan": {
    "id": 1,
    "name": "Basic Plan",
    "description": "Basic features for individuals",
    "price": "9.99",
    "billing_interval": "month"
  },
  "stripe_subscription_id": "sub_1234567890",
  "status": "active",
  "start_date": "2025-05-12T10:00:00Z",
  "end_date": null
}
```

### Cancel a subscription

```bash
curl -X DELETE http://localhost:8000/unsubscribe/1/
```

Response: HTTP 204 No Content

## Data Models

### Plan

- `name`: Name of the plan
- `description`: Description of the plan features
- `price`: Cost of the plan
- `billing_interval`: Billing frequency (month, year)
- `stripe_price_id`: ID of the price in Stripe

### Subscriber

- `name`: Customer name
- `email`: Customer email address
- `phone_number`: Customer phone number
- `stripe_customer_id`: ID of the customer in Stripe

### Subscription

- `subscriber`: Reference to the Subscriber
- `plan`: Reference to the Plan
- `stripe_subscription_id`: ID of the subscription in Stripe
- `status`: Current status of the subscription (active, canceled)
- `start_date`: When the subscription began
- `end_date`: When the subscription ended (if canceled)

## Stripe Integration

This API integrates with Stripe for payment processing. When a user subscribes:

1. A Stripe customer is created (if they don't already exist)
2. A Stripe subscription is created using the selected plan
3. Webhook events from Stripe (like subscription cancellation) are processed automatically

## Asynchronous Tasks

The API uses Celery for asynchronous tasks like:

- Sending welcome SMS messages when a new subscriber joins

## Error Handling

The API includes robust error handling:

- Validation errors for invalid input data
- Resource not found errors for invalid IDs
- Exception handling for Stripe API errors

## Security Considerations

- Environment variables should be used for sensitive information like API keys
- In production, ensure Stripe webhook verification is implemented
- SSL/TLS should be enabled for all API traffic

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -am 'Add feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
