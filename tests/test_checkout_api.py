from datetime import datetime
from urllib.parse import urlencode

import pytz
from django.test import Client, TestCase
from django.urls import reverse

from djpaddle.models import Checkout


class TestWebhook(TestCase):
    def _api_request(self, data):
        return Client().post(
            reverse("djpaddle:post_checkout_api"),
            data,
            content_type="application/x-www-form-urlencoded",
        )

    def test_checkout_api(self):
        completed = True
        data = {
            "id": "11111111-aaaa8f3706b5378-17fba8a806",
            "completed": str(completed).lower(),
            "passthrough": '{"organisation": "PKG-Deploy", "user_id": "1"}',
            "email": "pyematt@gmail.com",
            "created_at": "2020-05-22 23:42:02",
        }
        payload = urlencode(data)
        resp = self._api_request(payload)
        self.assertEqual(resp.status_code, 204)
        checkout = Checkout.objects.get(pk=data["id"])
        self.assertEqual(checkout.completed, completed)
        self.assertEqual(checkout.passthrough, data["passthrough"])
        self.assertEqual(checkout.email, data["email"])
        created = datetime.strptime(data["created_at"], "%Y-%m-%d %H:%M:%S")
        self.assertEqual(checkout.created_at, created.replace(tzinfo=pytz.UTC))

    def test_checkout_api_missing_not_required(self):
        completed = False
        data = {
            "id": "11111111-aaaa8f3706b5378-17fba8a806",
            "completed": str(completed).lower(),
            "passthrough": "",
            "email": "",
            "created_at": "2020-05-22 23:42:02",
        }
        payload = urlencode(data)
        resp = self._api_request(payload)
        self.assertEqual(resp.status_code, 204)
        checkout = Checkout.objects.get(pk=data["id"])
        self.assertEqual(checkout.completed, completed)
        self.assertEqual(checkout.passthrough, data["passthrough"])
        self.assertEqual(checkout.email, data["email"])
        created = datetime.strptime(data["created_at"], "%Y-%m-%d %H:%M:%S")
        self.assertEqual(checkout.created_at, created.replace(tzinfo=pytz.UTC))

    def test_checkout_api_missing_id(self):
        data = {
            "id": "",
            "completed": "true",
        }
        payload = urlencode(data)
        resp = self._api_request(payload)
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(Checkout.objects.count(), 0)

    def test_checkout_api_missing_completed(self):
        data = {
            "id": "11111111-aaaa8f3706b5378-17fba8a806",
            "created_at": "2020-05-22 23:42:02",
        }
        payload = urlencode(data)
        resp = self._api_request(payload)
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(Checkout.objects.count(), 0)

    def test_checkout_api_bad_date(self):
        data = {
            "id": "11111111-aaaa8f3706b5378-17fba8a806",
            "completed": "true",
            "created_at": "baddate",
        }
        payload = urlencode(data)
        resp = self._api_request(payload)
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(Checkout.objects.count(), 0)
