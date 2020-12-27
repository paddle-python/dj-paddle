import importlib
import threading

from . import settings

_cache = threading.local()
_cache.modules = {}


def _get_fn(fn, *args, **kwargs):
    mod_name, func_name = fn.rsplit(".", 1)
    try:
        cached_modules = _cache.modules
    except AttributeError:  # pragma: no cover
        # AttributeError: '_thread._local' object has no attribute 'modules'
        cached_modules = {}

    if mod_name not in cached_modules:
        cached_modules[mod_name] = importlib.import_module(mod_name)
    return getattr(cached_modules[mod_name], func_name)


def subscriber_by_payload(Subscriber, payload):
    """
    Map a subscriber to a subscription based on the given webhook payload.
    You can overwrite this function via settings.DJPADDLE_SUBSCRIBER_BY_PAYLOAD.

    must throw Subscriber.DoesNotExist in case the mapping failed.
    """
    if "email" not in payload:
        raise Subscriber.DoesNotExist("'email' missing in payload")
    return Subscriber.objects.get(email=payload["email"])


def subscriptions_by_subscriber(subscriber, queryset):
    """
    Filter subscriptions by subscriber. This function is used in order to
    find and link stale subscriptions. You can overwrite this function
    via settings.DJPADDLE_SUBSCRIPTIONS_BY_SUBSCRIBER.
    """
    return queryset.filter(email__iexact=subscriber.email)


def get_subscriber_by_payload(Subscriber, payload):
    """
    wrapper to retrieve and call the function referenced in settings.DJPADDLE_SUBSCRIBER_BY_PAYLOAD
    """
    return _get_fn(settings.DJPADDLE_SUBSCRIBER_BY_PAYLOAD)(Subscriber=Subscriber, payload=payload)


def get_subscriptions_by_subscriber(subscriber, queryset):
    """
    wrapper to retrieve and call the function referenced in settings.DJPADDLE_SUBSCRIPTIONS_BY_SUBSCRIBER
    """
    return _get_fn(settings.DJPADDLE_SUBSCRIPTIONS_BY_SUBSCRIBER)(subscriber=subscriber, queryset=queryset)
