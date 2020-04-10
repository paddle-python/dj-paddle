from django.db import models
from django.db.models.signals import post_save
from django.utils.translation import gettext_lazy as _
from django.dispatch import receiver
from django.utils import timezone

from . import settings, signals, api
from .fields import PaddleCurrencyCodeField


class PaddleBaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Price(PaddleBaseModel):
    plan = models.ForeignKey(
        "djpaddle.Plan", on_delete=models.CASCADE, related_name="prices"
    )
    currency = PaddleCurrencyCodeField()
    quantity = models.FloatField()
    recurring = models.BooleanField()

    def __str__(self):
        return " ".join([str(self.quantity), self.currency])

    class Meta:
        ordering = ["currency", "recurring"]
        unique_together = ("plan", "currency", "recurring")


class Plan(PaddleBaseModel):
    """
    'Plan' represents a Paddle subscription plan.
    """

    PADDLE_URI_LIST = "subscription/plans"

    BILLING_TYPE_DAY = "day"
    BILLING_TYPE_MONTH = "month"
    BILLING_TYPE_YEAR = "year"
    BILLING_TYPE = (
        (BILLING_TYPE_DAY, _("day")),
        (BILLING_TYPE_MONTH, _("month")),
        (BILLING_TYPE_YEAR, _("year")),
    )

    name = models.CharField(max_length=255)
    billing_type = models.CharField(choices=BILLING_TYPE, max_length=255)
    billing_period = models.IntegerField()
    trial_days = models.IntegerField(default=0)

    class Meta:
        ordering = ["created_at"]

    @classmethod
    def api_list(cls):
        return api.retrieve(uri=cls.PADDLE_URI_LIST)

    @classmethod
    def sync_from_paddle_data(cls, data):
        pk = data.pop("id", None)
        initial_price = data.pop("initial_price", [])
        recurring_price = data.pop("recurring_price", [])

        plan, _ = cls.objects.get_or_create(pk=pk, defaults=data)

        # drop all existing prices
        plan.prices.all().delete()

        Price.objects.bulk_create(
            # re-create initial prices
            [
                Price(
                    plan=plan,
                    currency=currency,
                    quantity=float(quantity),
                    recurring=False,
                )
                for currency, quantity in initial_price.items()
            ]
            # re-create initial prices
            + [
                Price(
                    plan=plan,
                    currency=currency,
                    quantity=float(quantity),
                    recurring=True,
                )
                for currency, quantity in recurring_price.items()
            ]
        )

        return plan

    def __str__(self):
        return "Plan <{}:{}>".format(self.name, str(self.id))


class Subscription(PaddleBaseModel):
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
    PADDLE_URI_LIST = 'subscription/users'

    id = models.TextField(primary_key=True)
    subscriber = models.ForeignKey(
        settings.DJPADDLE_SUBSCRIBER_MODEL,
        related_name="subscriptions",
        null=True,
        default=None,
        on_delete=models.CASCADE,
    )

    cancel_url = models.URLField()
    checkout_id = models.TextField()
    currency = models.CharField(max_length=3)
    email = models.EmailField()
    event_time = models.DateTimeField()
    marketing_consent = models.BooleanField()
    next_bill_date = models.DateTimeField(
        null=True, blank=True)
    passthrough = models.TextField()
    quantity = models.IntegerField()
    source = models.URLField()
    status = models.CharField(choices=STATUS, max_length=16)
    plan = models.ForeignKey("djpaddle.Plan", on_delete=models.CASCADE)
    unit_price = models.FloatField()
    update_url = models.URLField()

    class Meta:
        ordering = ["created_at"]

    @classmethod
    def api_list(cls):
        return api.retrieve(uri=cls.PADDLE_URI_LIST)

    @classmethod
    def sync_from_paddle_data(cls, data):
        pk = data.get('subscription_id', None)
        # First, find and drop current sub with this data.
        cls.objects.filter(pk=pk).delete()
        kwargs = {}

        try:
            kwargs['subscriber'] = settings.get_subscriber_model().objects.get(
                email=data["user_email"]
            )
        except settings.get_subscriber_model().DoesNotExist:
            pass

        try:
            kwargs['plan'] = Plan.objects.get(pk=data.get("plan_id"))
        except Plan.DoesNotExist:
            print("Skipping, plan not found.")
            return

        # Now, create object with this pk.
        sub = Subscription.objects.create(
            id=pk,
            cancel_url=data.get("cancel_url"),
            checkout_id="", # ???
            currency=data.get('last_payment').get("currency"),
            email=data.get("user_email"),
            event_time=timezone.now(), # ???
            marketing_consent=data.get('marketing_consent'),
            # next_bill_date can be null if user won't pay again...
            next_bill_date=data.get("next_payment", {}).get("date", None),
            passthrough="", # ???
            quantity=data.get("last_payment", {}).get("amount", 0),
            source="", # ???
            status=data.get("state"),
            unit_price=0.00, # ???
            update_url = data.get('update_url'),
            **kwargs
        )
        return sub

    @classmethod
    def _sanitize_webhook_payload(cls, payload):
        data = {}

        data["id"] = payload.pop("subscription_id", None)

        # transform `user_id` to subscriber ref
        data["subscriber"] = None
        subscriber_id = payload.pop("user_id", None)
        try:
            if subscriber_id not in ["", None]:
                data[
                    "subscriber"] = settings.get_subscriber_model().objects.get(
                    email=payload["email"]
                )
        except settings.get_subscriber_model().DoesNotExist:
            pass

        # transform `subscription_plan_id` to plan ref
        data["plan"] = None
        plan_id = payload.pop("subscription_plan_id", None)
        if plan_id not in ["", None]:
            data["plan"] = Plan.objects.get(pk=plan_id)

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
        return cls.objects.get_or_create(**data)

    @classmethod
    def update_by_payload(cls, payload):
        data = cls._sanitize_webhook_payload(payload)
        pk = data.pop("id")
        return cls.objects.update_or_create(pk=pk, defaults=data)

    def __str__(self):
        return "Subscription <{}:{}>".format(str(self.subscriber), str(self.id))


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
                subscriber=None, email__iexact=instance.email
            )
            subscriptions.update(subscriber=instance)
