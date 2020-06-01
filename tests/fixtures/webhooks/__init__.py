PLAN_ID = 1
FAKE_ALERT_TEST_SUBSCRIPTION_CREATED = {
    "alert_id": 1,
    "alert_name": "subscription_created",
    "cancel_url": "https://checkout.paddle.com/subscription/cancel?user=1&subscription=2&hash=aaaaaa",  # NOQA: E501
    "update_url": "https://checkout.paddle.com/subscription/update?user=5&subscription=4&hash=aaaaaa",  # NOQA: E501
    "checkout_id": "aaaa-1234",
    "currency": "EUR",
    "email": "gardner.wuckert@example.org",
    "event_time": "2020-01-13 19:19:18",
    "marketing_consent": 1,
    "next_bill_date": "2020-01-30",
    "passthrough": "",
    "quantity": 1,
    "source": "",
    "status": "active",
    "subscription_id": 1,
    "subscription_plan_id": PLAN_ID,
    "unit_price": 0,
    "user_id": 1,
}
FAKE_GET_PLAN_RESPONSE = [
    {
        "billing_period": 1,
        "billing_type": "day",
        "id": PLAN_ID,
        "initial_price": {"USD": "0.00"},
        "name": "djpaddle-plan-mock",
        "recurring_price": {"USD": "0.00"},
        "trial_days": 0,
    }
]
