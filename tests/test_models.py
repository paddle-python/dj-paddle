"""
These tests feel a little pointless but there is a minimum coverage
percentage...
"""
from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from djpaddle.models import Plan, Price, Subscription


class TestModelStrs(TestCase):
    def test_plan_str(self):
        pk = 1
        name = "test"
        plan = Plan.objects.create(
            pk=pk,
            name=name,
            billing_type="month",
            billing_period=1,
            trial_days=0,
        )
        self.assertEqual(str(plan), "{}:{}".format(name, str(pk)))

    def test_price_str(self):
        plan = Plan.objects.create(
            pk=1,
            name="name",
            billing_type="month",
            billing_period=1,
            trial_days=0,
        )
        quantity = 0.1
        currency = "USD"
        price = Price.objects.create(plan=plan, currency=currency, quantity=quantity, recurring=True)
        price_string = "{} {}".format(quantity, currency)
        self.assertEqual(str(price), price_string)

    def test_subscription_str(self):
        user = "test"
        user = User.objects.create(username=user)
        plan = Plan.objects.create(
            pk=1,
            name="name",
            billing_type="month",
            billing_period=1,
            trial_days=0,
        )
        pk = 1
        subscription = Subscription.objects.create(
            cancel_url="https://checkout.paddle.com/subscription/cancel?user=1&subscription=2&hash=aaaaaa",  # NOQA: E501
            checkout_id="1",
            created_at=timezone.now(),
            currency="EUR",
            email="test@example.com",
            event_time=timezone.now(),
            id=pk,
            marketing_consent=True,
            next_bill_date=timezone.now(),
            passthrough="",
            plan=plan,
            quantity=1,
            source="",
            status="active",
            subscriber=user,
            unit_price=0.0,
            update_url="https://checkout.paddle.com/subscription/update?user=5&subscription=4&hash=aaaaaa",  # NOQA: E501
            updated_at=timezone.now(),
        )
        self.assertEqual(str(subscription), "{}:{}".format(user, str(pk)))
