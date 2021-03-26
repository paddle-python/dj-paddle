from django.http import HttpRequest
from django.test.testcases import TestCase

from djpaddle import context_processors

from . import settings


class TestContextProcessors(TestCase):
    def test_context_processor_vendor_id(self):
        result = context_processors.vendor_id(HttpRequest())
        expected_result = {
            "DJPADDLE_VENDOR_ID": settings.DJPADDLE_VENDOR_ID,
        }
        self.assertDictEqual(expected_result, result)

    def test_context_processor_sandbox(self):
        sandbox = getattr(settings, "DJPADDLE_SANDBOX", False)
        result = context_processors.sandbox(HttpRequest())
        expected_result = {
            "DJPADDLE_SANDBOX": sandbox,
        }
        self.assertDictEqual(expected_result, result)
