import django.dispatch

# Subscription Alerts
subscription_created = django.dispatch.Signal(providing_args=["payload"])
subscription_updated = django.dispatch.Signal(providing_args=["payload"])
subscription_cancelled = django.dispatch.Signal(providing_args=["payload"])
subscription_payment_succeeded = django.dispatch.Signal(providing_args=["payload"])
subscription_payment_failed = django.dispatch.Signal(providing_args=["payload"])
subscription_payment_refunded = django.dispatch.Signal(providing_args=["payload"])

# One-off Purchases
locker_processed = django.dispatch.Signal(providing_args=["payload"])
payment_succeeded = django.dispatch.Signal(providing_args=["payload"])
payment_refunded = django.dispatch.Signal(providing_args=["payload"])

# Risk & Dispute Alerts
payment_dispute_created = django.dispatch.Signal(providing_args=["payload"])
payment_dispute_closed = django.dispatch.Signal(providing_args=["payload"])
high_risk_transaction_created = django.dispatch.Signal(providing_args=["payload"])
high_risk_transaction_updated = django.dispatch.Signal(providing_args=["payload"])

# Payout Alerts
transfer_created = django.dispatch.Signal(providing_args=["payload"])
transfer_paid = django.dispatch.Signal(providing_args=["payload"])

# Audience Alerts
new_audience_member = django.dispatch.Signal(providing_args=["payload"])
update_audience_member = django.dispatch.Signal(providing_args=["payload"])
