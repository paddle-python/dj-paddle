from django.db import models
from django.db.models.signals import post_save
from django.utils.translation import gettext_lazy as _
from django.dispatch import receiver

from . import settings, signals


class Subscription(models.Model):
    """
    'Subscription' represents a Paddle subscription.

    They are automatically updated on behalf of the webhook calls 'subscription_created',
    'subscription_updated' and 'subscription_cancelled'.

    Stale subscriptions that are not associated with a subscriber are being linked by comparing
    the email addresses of the subscriber model and the subscription. Linking is optional and can
    be configured through the settings ('DJPADDLE_LINK_STALE_SUBSCRIPTIONS').
    """

    STATUS_ACTIVE = "active"
    STATUS_TRIALING = "trialing"
    STATUS_PAST_DUE = "past_due"
    STATUS_PAUSED = "paused"
    STATUS_DELETED = "deleted"
    STATUS = (
        (STATUS_ACTIVE, _("active")),
        (STATUS_TRIALING, _("trialing")),
        (STATUS_PAST_DUE, _("past due")),
        (STATUS_PAUSED, _("paused")),
        (STATUS_DELETED, _("deleted")),
    )

    id = models.CharField(max_length=32, primary_key=True)
    subscriber = models.ForeignKey(
        settings.DJPADDLE_SUBSCRIBER_MODEL,
        related_name="subscriptions",
        null=True,
        default=None,
        on_delete=models.CASCADE,
    )

    cancel_url = models.URLField()
    checkout_id = models.CharField(max_length=32)
    currency = models.CharField(max_length=3)
    email = models.EmailField()
    event_time = models.DateTimeField()
    marketing_consent = models.BooleanField()
    next_bill_date = models.DateTimeField()
    passthrough = models.TextField()
    quantity = models.IntegerField()
    source = models.URLField()
    status = models.CharField(choices=STATUS, max_length=16)
    subscription_plan_id = models.CharField(max_length=32)
    unit_price = models.FloatField()
    update_url = models.URLField()

    @classmethod
    def _sanitize_webhook_payload(cls, payload):
        data = {}

        data["id"] = data.pop("subscription_id", None)

        # transform `user_id` to subscriber ref
        data["subscriber"] = None
        subscriber_id = data.pop("user_id", None)
        if subscriber_id not in ["", None]:
            data["subscriber"] = settings.get_subscriber_model().objects.get(
                pk=subscriber_id
            )

        # sanitize fields
        valid_field_names = [field.name for field in cls._meta.get_fields()]
        for key, value in payload.items():
            # e.g. 'new_status' --> 'status'
            if key.startswith("new_"):
                key = key[4:]

            if key in valid_field_names:
                data[key] = value

        return data

    @classmethod
    def from_subscription_created(cls, payload):
        data = cls._sanitize_webhook_payload(payload)
        return cls(**data)

    @classmethod
    def update_by_payload(cls, payload):
        data = cls._sanitize_webhook_payload(payload)
        pk = data.pop("id")
        return cls.objects.update_or_create(pk, defaults=data)


@receiver(signals.subscription_created)
def on_subscription_created(sender, payload, *args, **kwargs):
    Subscription.from_subscription_created(payload)


@receiver(signals.subscription_updated)
def on_subscription_updated(sender, payload, *args, **kwargs):
    Subscription.update_by_payload(payload)


@receiver(signals.subscription_cancelled)
def on_subscription_cancelled(sender, payload, *args, **kwargs):
    Subscription.update_by_payload(payload)


if settings.DJPADDLE_LINK_STALE_SUBSCRIPTIONS:

    @receiver(post_save, sender=settings.DJPADDLE_SUBSCRIBER_MODEL)
    def link_stale_subscriptions_to_subscriber(
        sender, instance, created, *args, **kwargs
    ):
        if created:
            subscriptions = Subscription.objects.filter(
                user=None, email__iexact=instance.email
            )
            subscriptions.update(user=instance)
