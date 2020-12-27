import django.dispatch

# Subscription Alerts
subscription_created = django.dispatch.Signal()
subscription_updated = django.dispatch.Signal()
subscription_cancelled = django.dispatch.Signal()
subscription_payment_succeeded = django.dispatch.Signal()
subscription_payment_failed = django.dispatch.Signal()
subscription_payment_refunded = django.dispatch.Signal()

# One-off Purchases
locker_processed = django.dispatch.Signal()
payment_succeeded = django.dispatch.Signal()
payment_refunded = django.dispatch.Signal()

# Risk & Dispute Alerts
payment_dispute_created = django.dispatch.Signal()
payment_dispute_closed = django.dispatch.Signal()
high_risk_transaction_created = django.dispatch.Signal()
high_risk_transaction_updated = django.dispatch.Signal()

# Payout Alerts
transfer_created = django.dispatch.Signal()
transfer_paid = django.dispatch.Signal()

# Audience Alerts
new_audience_member = django.dispatch.Signal()
update_audience_member = django.dispatch.Signal()
