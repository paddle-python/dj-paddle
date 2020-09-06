from datetime import datetime
from urllib.parse import urlencode

import pytz
from django.test import Client, TestCase
from django.urls import reverse

from djpaddle.models import Checkout
from djpaddle.utils import PADDLE_DATETIME_FORMAT


class TestPostCheckoutApi(TestCase):
    def _api_request(self, url, data):
        return Client().post(url, data, content_type="application/x-www-form-urlencoded",)

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
        url = reverse("djpaddle:post_checkout_api")
        resp = self._api_request(url, payload)
        self.assertEqual(resp.status_code, 204)
        checkout = Checkout.objects.get(pk=data["id"])
        self.assertEqual(checkout.completed, completed)
        self.assertEqual(checkout.passthrough, data["passthrough"])
        self.assertEqual(checkout.email, data["email"])
        created = datetime.strptime(data["created_at"], PADDLE_DATETIME_FORMAT)
        self.assertEqual(checkout.created_at, created.replace(tzinfo=pytz.UTC))

    def test_checkout_api_next_redirect(self):
        completed = True
        data = {
            "id": "11111111-aaaa8f3706b5378-17fba8a806",
            "completed": str(completed).lower(),
            "passthrough": '{"organisation": "PKG-Deploy", "user_id": "1"}',
            "email": "pyematt@gmail.com",
            "created_at": "2020-05-22 23:42:02",
        }
        payload = urlencode(data)

        redirect_url = "/someurl"
        url = reverse("djpaddle:post_checkout_api")
        url = "{0}?next={1}".format(url, redirect_url)
        resp = self._api_request(url, payload)
        self.assertEqual(resp.status_code, 200)
        response = resp.json()
        redirect_url = "{0}?checkout={1}".format(redirect_url, data["id"])
        self.assertEqual(response["redirect_url"], redirect_url)
        checkout = Checkout.objects.get(pk=data["id"])
        self.assertEqual(checkout.completed, completed)
        self.assertEqual(checkout.passthrough, data["passthrough"])
        self.assertEqual(checkout.email, data["email"])
        created = datetime.strptime(data["created_at"], PADDLE_DATETIME_FORMAT)
        self.assertEqual(checkout.created_at, created.replace(tzinfo=pytz.UTC))

    def test_checkout_api_paddle_redirect(self):
        completed = True
        redirect_url = "http://example.com/checkout/success"
        data = {
            "id": "11111111-aaaa8f3706b5378-17fba8a806",
            "completed": str(completed).lower(),
            "passthrough": '{"organisation": "PKG-Deploy", "user_id": "1"}',
            "email": "pyematt@gmail.com",
            "created_at": "2020-05-22 23:42:02",
            "redirect_url": redirect_url,
        }
        payload = urlencode(data)

        url = reverse("djpaddle:post_checkout_api")
        resp = self._api_request(url, payload)
        self.assertEqual(resp.status_code, 200)
        response = resp.json()
        redirect_url = "{0}?checkout={1}".format(redirect_url, data["id"])
        self.assertEqual(response["redirect_url"], redirect_url)
        checkout = Checkout.objects.get(pk=data["id"])
        self.assertEqual(checkout.completed, completed)
        self.assertEqual(checkout.passthrough, data["passthrough"])
        self.assertEqual(checkout.email, data["email"])
        created = datetime.strptime(data["created_at"], PADDLE_DATETIME_FORMAT)
        self.assertEqual(checkout.created_at, created.replace(tzinfo=pytz.UTC))

    def test_checkout_api_next_and_paddle_redirect(self):
        completed = True
        redirect_url = "http://example.com/checkout/success"
        data = {
            "id": "11111111-aaaa8f3706b5378-17fba8a806",
            "completed": str(completed).lower(),
            "passthrough": '{"organisation": "PKG-Deploy", "user_id": "1"}',
            "email": "pyematt@gmail.com",
            "created_at": "2020-05-22 23:42:02",
            "redirect_url": redirect_url,
        }
        payload = urlencode(data)

        redirect_url = "/someurl"
        url = reverse("djpaddle:post_checkout_api")
        url = "{0}?next={1}".format(url, redirect_url)
        resp = self._api_request(url, payload)
        self.assertEqual(resp.status_code, 200)
        response = resp.json()
        redirect_url = "{0}?checkout={1}".format(redirect_url, data["id"])
        self.assertEqual(response["redirect_url"], redirect_url)
        checkout = Checkout.objects.get(pk=data["id"])
        self.assertEqual(checkout.completed, completed)
        self.assertEqual(checkout.passthrough, data["passthrough"])
        self.assertEqual(checkout.email, data["email"])
        created = datetime.strptime(data["created_at"], PADDLE_DATETIME_FORMAT)
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
        url = reverse("djpaddle:post_checkout_api")
        resp = self._api_request(url, payload)
        self.assertEqual(resp.status_code, 204)
        checkout = Checkout.objects.get(pk=data["id"])
        self.assertEqual(checkout.completed, completed)
        self.assertEqual(checkout.passthrough, data["passthrough"])
        self.assertEqual(checkout.email, data["email"])
        created = datetime.strptime(data["created_at"], PADDLE_DATETIME_FORMAT)
        self.assertEqual(checkout.created_at, created.replace(tzinfo=pytz.UTC))

    def test_checkout_api_missing_id(self):
        data = {
            "id": "",
            "completed": "true",
        }
        payload = urlencode(data)
        url = reverse("djpaddle:post_checkout_api")
        resp = self._api_request(url, payload)
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(Checkout.objects.count(), 0)

    def test_checkout_api_missing_completed(self):
        data = {
            "id": "11111111-aaaa8f3706b5378-17fba8a806",
            "created_at": "2020-05-22 23:42:02",
        }
        payload = urlencode(data)
        url = reverse("djpaddle:post_checkout_api")
        resp = self._api_request(url, payload)
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(Checkout.objects.count(), 0)

    def test_checkout_api_bad_date(self):
        data = {
            "id": "11111111-aaaa8f3706b5378-17fba8a806",
            "completed": "true",
            "created_at": "baddate",
        }
        payload = urlencode(data)
        url = reverse("djpaddle:post_checkout_api")
        resp = self._api_request(url, payload)
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(Checkout.objects.count(), 0)
