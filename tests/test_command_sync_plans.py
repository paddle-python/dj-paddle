from unittest import mock

from django.core.management import call_command
from django.test import TestCase

from djpaddle.models import Plan

FAKE_PLAN_API_RESPONSE = [
    {
        "billing_period": 1,
        "billing_type": "day",
        "id": 10,
        "initial_price": {"GBP": "0.00"},
        "name": "Plan 10",
        "recurring_price": {"GBP": "0.00"},
        "trial_days": 0,
    },
    {
        "billing_period": 1,
        "billing_type": "day",
        "id": 11,
        "initial_price": {"GBP": "0.00"},
        "name": "Plan 11",
        "recurring_price": {"GBP": "0.00"},
        "trial_days": 0,
    },
    {
        "billing_period": 1,
        "billing_type": "day",
        "id": 12,
        "initial_price": {"GBP": "0.00"},
        "name": "Plan 12",
        "recurring_price": {"GBP": "0.00"},
        "trial_days": 0,
    },
]


class TestSyncPlans(TestCase):
    @mock.patch("djpaddle.api.requests.request")
    def test_command(self, request_mock):
        data = {"response": FAKE_PLAN_API_RESPONSE}
        request_mock.return_value = mock.Mock(ok=True)
        request_mock.return_value.json.return_value = data

        args = []
        opts = {}
        call_command("djpaddle_sync_plans_from_paddle", *args, **opts)

        plans = Plan.objects.all()
        self.assertEqual(plans.count(), len(FAKE_PLAN_API_RESPONSE))
        for paddle_plan in FAKE_PLAN_API_RESPONSE:
            db_plan = Plan.objects.get(name=paddle_plan["name"])
            self.assertEqual(db_plan.billing_type, paddle_plan["billing_type"])
            self.assertEqual(db_plan.billing_period, paddle_plan["billing_period"])
            self.assertEqual(db_plan.trial_days, paddle_plan["trial_days"])
