from copy import deepcopy
from os.path import abspath, dirname, join
from unittest import mock
from urllib.parse import parse_qs

from django.test import Client, TestCase
from django.urls import reverse

from djpaddle.models import Plan, Subscription

from . import FAKE_ALERT_TEST_SUBSCRIPTION_CREATED


class TestWebhook(TestCase):
    def _send_alert(self, data):
        return Client().post(reverse("djpaddle:webhook"), data)

    def _send_alert_urlencoded(self, data):
        return Client().post(
            reverse("djpaddle:webhook"),
            data,
            content_type="application/x-www-form-urlencoded",
        )

    def load_fixture(self, fixture_name):
        this_directory = abspath(dirname(__file__))
        fixture_directory = join(this_directory, "fixtures")
        fixture_path = join(fixture_directory, fixture_name)
        with open(fixture_path, "r") as file:
            return file.read()

    @mock.patch("djpaddle.views.is_valid_webhook", return_value=True)
    def test_webhook_is_valid_alert(self, is_valid_webhook):
        valid_alert = deepcopy(FAKE_ALERT_TEST_SUBSCRIPTION_CREATED)
        valid_alert["p_signature"] = "valid-signature"
        pk = 1
        name = "monthly-subscription"
        Plan.objects.create(
            pk=pk, name=name, billing_type="month", billing_period=1, trial_days=0,
        )
        resp = self._send_alert(valid_alert)
        self.assertTrue(is_valid_webhook.called)
        self.assertEqual(resp.status_code, 200)

    def test_webhook_is_invalid_signature(self):
        invalid_alert = deepcopy(FAKE_ALERT_TEST_SUBSCRIPTION_CREATED)
        invalid_alert["p_signature"] = "invalid-signature"

        resp = self._send_alert(invalid_alert)
        self.assertEqual(resp.status_code, 400)

    @mock.patch("djpaddle.views.is_valid_webhook", return_value=True)
    def test_webhook_bad_request_missing_alert_name(self, is_valid_webhook):
        payload = deepcopy(FAKE_ALERT_TEST_SUBSCRIPTION_CREATED)
        del payload["alert_name"]
        response = self._send_alert(payload)
        self.assertEqual(response.status_code, 400)

    @mock.patch("djpaddle.views.is_valid_webhook", return_value=True)
    def test_webhook_not_supported_hook(self, is_valid_webhook):
        payload = deepcopy(FAKE_ALERT_TEST_SUBSCRIPTION_CREATED)
        payload["alert_name"] = "not_and_valid_hook"
        response = self._send_alert(payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Subscription.objects.all().count(), 0)

    @mock.patch("djpaddle.views.is_valid_webhook", return_value=True)
    def test_subscription_created_webhook(self, is_valid_webhook):
        payload = self.load_fixture("subscription_created.txt")
        data = parse_qs(payload)
        Plan.objects.create(
            pk=int(data["subscription_plan_id"][0]),
            name="monthly-subscription",
            billing_type="month",
            billing_period=1,
            trial_days=0,
        )
        self._send_alert_urlencoded(payload)
        subscription = Subscription.objects.get(email=data["email"][0])
        self.assertEqual(subscription.email, "branson.nikolaus@example.org")

    @mock.patch("djpaddle.views.is_valid_webhook", return_value=True)
    def test_subscription_updated_webhook(self, is_valid_webhook):
        create_payload = self.load_fixture("subscription_created.txt")
        create_data = parse_qs(create_payload)
        Plan.objects.create(
            pk=int(create_data["subscription_plan_id"][0]),
            name="monthly-subscription",
            billing_type="month",
            billing_period=1,
            trial_days=0,
        )
        self._send_alert_urlencoded(create_payload)
        subscription = Subscription.objects.get(email=create_data["email"][0])
        self.assertEqual(subscription.email, "branson.nikolaus@example.org")
        self.assertEqual(subscription.quantity, int(create_data["quantity"][0]))

        update_payload = self.load_fixture("subscription_updated.txt")
        updated_data = parse_qs(update_payload)
        self._send_alert_urlencoded(update_payload)
        subscription = Subscription.objects.get(id=subscription.id)
        self.assertEqual(subscription.email, "branson.nikolaus@example.org")
        self.assertEqual(subscription.quantity, int(updated_data["new_quantity"][0]))

    @mock.patch("djpaddle.views.is_valid_webhook", return_value=True)
    def test_subscription_cancelled_webhook(self, is_valid_webhook):
        create_payload = self.load_fixture("subscription_created.txt")
        create_data = parse_qs(create_payload)
        Plan.objects.create(
            pk=int(create_data["subscription_plan_id"][0]),
            name="monthly-subscription",
            billing_type="month",
            billing_period=1,
            trial_days=0,
        )
        self._send_alert_urlencoded(create_payload)
        subscription = Subscription.objects.get(email=create_data["email"][0])
        self.assertEqual(subscription.status, create_data["status"][0])

        delete_payload = self.load_fixture("subscription_cancelled.txt")
        delete_data = parse_qs(delete_payload)
        self.assertEqual(delete_data["status"][0], "deleted")

        self._send_alert_urlencoded(delete_payload)
        subscription = Subscription.objects.get(id=subscription.id)
        self.assertEqual(subscription.status, delete_data["status"][0])
