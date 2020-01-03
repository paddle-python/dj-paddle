from django.views.generic import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseBadRequest

from .utils import is_valid_webhook
from . import signals


@method_decorator(csrf_exempt, name="dispatch")
class PaddleWebhookView(View):
    SUPPORTED_WEBHOOKS = (
        # Subscription Alerts
        "subscription_created",
        "subscription_updated",
        "subscription_cancelled",
        "subscription_payment_succeeded",
        "subscription_payment_failed",
        "subscription_payment_refunded",
        # One-off Purchases
        "locker_processed",
        "payment_succeeded",
        "payment_refunded",
        # Risk & Dispute Alerts
        "payment_dispute_created",
        "payment_dispute_closed",
        "high_risk_transaction_created",
        "high_risk_transaction_updated",
        # Payout Alerts
        "transfer_created",
        "transfer_paid",
        # Audience Alerts
        "new_audience_member",
        "update_audience_member",
    )

    def post(self, request, *args, **kwargs):
        """
        handle paddle webhook requests by
        - validating the payload signature
        - sending a django signal for each of the SUPPORTED_WEBHOOKS
        """
        payload = request.POST.dict()

        if not is_valid_webhook(payload):
            return HttpResponseBadRequest("webhook validation failed")

        alert_name = payload.get("alert_name", None)
        if alert_name is None:
            return HttpResponseBadRequest("'alert_name' missing")

        if alert_name in self.SUPPORTED_WEBHOOKS:
            signal = getattr(signals, alert_name, None)
            if signal is not None:
                signal.send(sender=self.__class__, payload=payload)

        return HttpResponse()


paddle_webhook_view = PaddleWebhookView.as_view()
