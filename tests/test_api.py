from unittest import mock

from django.conf import settings
from django.test import TestCase

from djpaddle import api


class TestAPIRequest(TestCase):
    @mock.patch("djpaddle.api.requests.request")
    def test_api_request_returns_response(self, request_mock):
        data = {"response": ["response-data"]}
        request_mock.return_value = mock.Mock(ok=True)
        request_mock.return_value.json.return_value = data

        response = api.retrieve(uri="uri")
        self.assertEqual(data["response"], response)

    @mock.patch("djpaddle.api.requests.request")
    def test_api_request_raises_on_missing_response(self, request_mock):
        request_mock.return_value = mock.Mock(ok=True)
        request_mock.return_value.json.return_value = {}

        self.assertRaises(api.APIException, api.api_request, method="get", uri="uri")

    @mock.patch("djpaddle.api.requests.request")
    def test_api_request_raises_on_error(self, request_mock):
        request_mock.return_value = mock.Mock(ok=True)
        error_response = {"error": {"code": "1", "message": "Bad"}}
        request_mock.return_value.json.return_value = error_response

        self.assertRaises(api.APIError, api.api_request, method="get", uri="uri")

    @mock.patch("djpaddle.api.requests.request")
    def test_api_request_assert_authentication(self, request_mock):
        data = {"response": ["response-data"]}
        request_mock.return_value = mock.Mock(ok=True)
        request_mock.return_value.json.return_value = data

        api.api_request(method="get", uri="uri", data={"fake": "data"})

        args, kwargs = request_mock.call_args
        self.assertIn("json", kwargs)
        payload = kwargs["json"]

        self.assertIn("vendor_id", payload)
        self.assertEqual(payload["vendor_id"], settings.DJPADDLE_VENDOR_ID)
        self.assertIn("vendor_auth_code", payload)
        self.assertEqual(payload["vendor_auth_code"], settings.DJPADDLE_API_KEY)
