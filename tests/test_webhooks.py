from copy import deepcopy
from unittest import mock

from django.conf import settings
from django.urls import reverse
from django.test import TestCase, Client

from . import FAKE_ALERT_TEST_SUBSCRIPTION_CREATED
from djpaddle.models import Plan, Subscription


class TestWebhook(TestCase):
    def _send_alert(self, data):
        return Client().post(reverse("djpaddle:webhook"), data)

    @mock.patch("djpaddle.views.is_valid_webhook", return_value=True)
    def test_webhook_is_valid_alert(self, is_valid_webhook):
        valid_alert = deepcopy(FAKE_ALERT_TEST_SUBSCRIPTION_CREATED)
        valid_alert["p_signature"] = "valid-signature"
        plan = Plan.objects.create(pk=1, name="monthly-subscription", billing_type="month", billing_period=1, trial_days=0)

        resp = self._send_alert(valid_alert)
        self.assertTrue(is_valid_webhook.called)
        self.assertEqual(resp.status_code, 200)

    def test_webhook_is_invalid_signature(self):
        invalid_alert = deepcopy(FAKE_ALERT_TEST_SUBSCRIPTION_CREATED)
        invalid_alert["p_signature"] = "invalid-signature"

        resp = self._send_alert(invalid_alert)
        self.assertEqual(resp.status_code, 400)

    @mock.patch("djpaddle.views.is_valid_webhook", return_value=True)
    def test_subscription_created_webhook(self, is_valid_webhook):
        payload = deepcopy(FAKE_ALERT_TEST_SUBSCRIPTION_CREATED)
        payload["p_signature"] = "valid-signature"
        plan = Plan.objects.create(pk=1, name="monthly-subscription", billing_type="month", billing_period=1, trial_days=0)

        resp = self._send_alert(payload)
        subscription = Subscription.objects.get(email=payload["email"])
        self.assertEqual(subscription.email, "gardner.wuckert@example.org")