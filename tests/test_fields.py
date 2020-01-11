from django.test.testcases import TestCase

from djpaddle.fields import PaddleCurrencyCodeField


class TestPaddleCurrencyField(TestCase):
    currency = PaddleCurrencyCodeField(name="currency")

    def test_currency_code_field_is_three_letter_iso(self):
        self.assertEqual(3, self.currency.max_length)
