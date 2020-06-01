from copy import deepcopy
from datetime import datetime, timedelta
from os.path import abspath, dirname, join
from unittest import mock
from urllib.parse import parse_qs, urlencode
from uuid import uuid4

import pytest
from django.test import Client, TestCase
from django.urls import reverse

from djpaddle.models import Plan, Subscription
from djpaddle.utils import PADDLE_DATE_FORMAT, PADDLE_DATETIME_FORMAT

from .fixtures.webhooks import (
    FAKE_ALERT_TEST_SUBSCRIPTION_CREATED,
    FAKE_GET_PLAN_RESPONSE,
)


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
        fixture_directory = join(fixture_directory, "webhooks")
        fixture_path = join(fixture_directory, fixture_name)
        with open(fixture_path, "r") as file:
            return file.read()

    @mock.patch("djpaddle.views.is_valid_webhook", return_value=True)
    def test_webhook_is_valid_alert(self, is_valid_webhook):
        valid_alert = deepcopy(FAKE_ALERT_TEST_SUBSCRIPTION_CREATED)
        valid_alert["p_signature"] = "valid-signature"
        name = "monthly-subscription"
        Plan.objects.create(
            pk=valid_alert["subscription_plan_id"],
            name=name,
            billing_type="month",
            billing_period=1,
            trial_days=0,
        )
        resp = self._send_alert(valid_alert)
        self.assertTrue(is_valid_webhook.called)
        self.assertEqual(resp.status_code, 200)
        subscriptions = Subscription.objects.all()
        self.assertEqual(subscriptions.count(), 1)
        subscription = subscriptions[0]
        self.assertEqual(subscription.cancel_url, valid_alert["cancel_url"])
        self.assertEqual(subscription.checkout_id, valid_alert["checkout_id"])
        self.assertEqual(subscription.currency, valid_alert["currency"])
        self.assertEqual(subscription.email, valid_alert["email"])
        event_time = subscription.event_time.strftime(PADDLE_DATETIME_FORMAT)
        self.assertEqual(event_time, valid_alert["event_time"])
        self.assertEqual(subscription.id, str(valid_alert["subscription_id"]))
        self.assertEqual(
            subscription.marketing_consent, valid_alert["marketing_consent"]
        )
        next_bill_date = subscription.next_bill_date.strftime(PADDLE_DATE_FORMAT)
        self.assertEqual(next_bill_date, valid_alert["next_bill_date"])
        self.assertEqual(subscription.passthrough, valid_alert["passthrough"])
        self.assertEqual(subscription.plan_id, valid_alert["subscription_plan_id"])
        self.assertEqual(subscription.quantity, valid_alert["quantity"])
        self.assertEqual(subscription.source, valid_alert["source"])
        self.assertEqual(subscription.status, valid_alert["status"])
        self.assertEqual(subscription.unit_price, valid_alert["unit_price"])
        self.assertEqual(subscription.update_url, valid_alert["update_url"])

    @mock.patch("djpaddle.views.is_valid_webhook", return_value=True)
    @mock.patch(
        "djpaddle.models.Paddle.list_plans", return_value=FAKE_GET_PLAN_RESPONSE
    )
    def test_webhook_missing_plan(self, is_valid_webhook, plan_api_get):
        valid_alert = deepcopy(FAKE_ALERT_TEST_SUBSCRIPTION_CREATED)
        valid_alert["p_signature"] = "valid-signature"
        with pytest.raises(Plan.DoesNotExist):
            Plan.objects.get(id=valid_alert["subscription_plan_id"])
        resp = self._send_alert(valid_alert)
        self.assertTrue(is_valid_webhook.called)
        self.assertEqual(resp.status_code, 200)
        plan = Plan.objects.get(id=valid_alert["subscription_plan_id"])
        self.assertEqual(plan.name, FAKE_GET_PLAN_RESPONSE[0]["name"])

    @mock.patch("djpaddle.views.is_valid_webhook", return_value=True)
    def test_webhook_missing_subscriber(self, is_valid_webhook):
        valid_alert = deepcopy(FAKE_ALERT_TEST_SUBSCRIPTION_CREATED)
        valid_alert["p_signature"] = "valid-signature"
        valid_alert["email"] = "{0}@example.com".format(str(uuid4()))
        Plan.objects.create(
            pk=valid_alert["subscription_plan_id"],
            name="test_webhook_missing_plan",
            billing_type="month",
            billing_period=1,
            trial_days=0,
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

        update_payload = self.load_fixture("subscription_updated.txt")
        updated_data = parse_qs(update_payload)
        self._send_alert_urlencoded(update_payload)
        subscription = Subscription.objects.get(email=create_data["email"][0])
        self.assertEqual(subscription.email, "branson.nikolaus@example.org")
        self.assertEqual(subscription.quantity, int(updated_data["new_quantity"][0]))
        subscriptions = Subscription.objects.all()
        self.assertEqual(subscriptions.count(), 1)

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

    @mock.patch("djpaddle.views.is_valid_webhook", return_value=True)
    def test_subscription_updated_webhook_previous_event(self, is_valid_webhook):
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

        update_payload = self.load_fixture("subscription_updated.txt")

        # parse_qs returns all values as lists, urlencode then takes the lists
        # and creates bad form data. So we flattern single list elements
        updated_data = {}
        for key, value in parse_qs(update_payload).items():
            if isinstance(value, list) and len(value) == 1:
                updated_data[key] = value[0]
            else:
                updated_data[key] = value

        subscription_id = updated_data["subscription_id"]
        subscription = Subscription.objects.get(pk=subscription_id)
        self.assertEqual(subscription.status, "active")

        event_time = updated_data["event_time"]
        event_time = datetime.strptime(event_time, PADDLE_DATETIME_FORMAT)
        event_time = event_time - timedelta(days=1)
        updated_data["event_time"] = event_time.strftime(PADDLE_DATETIME_FORMAT)
        updated_data["status"] = "paused"

        updated_payload = urlencode(updated_data)
        self._send_alert_urlencoded(updated_payload)
        subscription = Subscription.objects.get(pk=subscription_id)
        self.assertEqual(subscription.status, "active")
