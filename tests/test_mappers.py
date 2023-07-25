from django.test.testcases import TestCase
from django.utils import timezone

from djpaddle import settings, mappers
from djpaddle.models import Plan, Subscription


class TestPaddleMappers(TestCase):
    def test_get_subscriber_by_payload_does_not_exist(self):
        Subscriber = settings.get_subscriber_model()
        payload = {"email": "nonexistent@email.com"}

        with self.assertRaises(Subscriber.DoesNotExist):
            mappers.get_subscriber_by_payload(Subscriber, payload)

    def test_get_subscriber_by_payload(self):
        Subscriber = settings.get_subscriber_model()
        subscriber = Subscriber.objects.create(username="user", email="test@example.com")
        payload = {"email": "test@example.com"}
        fetched_subscriber = mappers.get_subscriber_by_payload(Subscriber, payload)
        self.assertEqual(fetched_subscriber.email, subscriber.email)

    def test_get_subscriber_by_payload_case_sensitive(self):
        Subscriber = settings.get_subscriber_model()
        subscriber = Subscriber.objects.create(username="user", email="Test@example.com")
        payload = {"email": "test@example.com"}
        fetched_subscriber = mappers.get_subscriber_by_payload(Subscriber, payload)
        self.assertEqual(fetched_subscriber.email, subscriber.email)

    def test_get_subscriber_by_payload_missing_email(self):
        Subscriber = settings.get_subscriber_model()
        payload = {"not-email": "nonexistent@email.com"}

        with self.assertRaises(Subscriber.DoesNotExist):
            mappers.get_subscriber_by_payload(Subscriber, payload)

    def test_get_subscriptions_by_subscriber(self):
        Subscriber = settings.get_subscriber_model()
        subscriber = Subscriber.objects.create(username="user", email="test@example.com")

        plan = Plan.objects.create(
            pk=1,
            name="name",
            billing_type="month",
            billing_period=1,
            trial_days=0,
        )
        Subscription.objects.create(
            cancel_url="https://checkout.paddle.com/subscription/cancel?user=1&subscription=2&hash=aaaaaa",  # NOQA: E501
            checkout_id="1",
            created_at=timezone.now(),
            currency="EUR",
            email="test@example.com",
            event_time=timezone.now(),
            id=1,
            marketing_consent=True,
            next_bill_date=timezone.now(),
            passthrough="",
            plan=plan,
            quantity=1,
            source="",
            status="active",
            subscriber=None,
            unit_price=0.0,
            update_url="https://checkout.paddle.com/subscription/update?user=5&subscription=4&hash=aaaaaa",  # NOQA: E501
            updated_at=timezone.now(),
        )

        subscriptions = mappers.get_subscriptions_by_subscriber(subscriber, Subscription.objects)
        self.assertEqual(1, len(subscriptions.all()))
