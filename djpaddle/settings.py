from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.apps import apps as django_apps


DJPADDLE_API_BASE = getattr(
    settings, "DJPADDLE_API_BASE", "https://vendors.paddle.com/api/2.0/"
)


# can be found at https://vendors.paddle.com/authentication
DJPADDLE_VENDOR_ID = getattr(settings, "DJPADDLE_VENDOR_ID", None)

# create one at https://vendors.paddle.com/authentication
DJPADDLE_API_KEY = getattr(settings, "DJPADDLE_API_KEY", None)

# can be found at https://vendors.paddle.com/public-key
DJPADDLE_PUBLIC_KEY = getattr(settings, "DJPADDLE_PUBLIC_KEY", None)
if DJPADDLE_PUBLIC_KEY is None:
    raise ImproperlyConfigured("'DJPADDLE_PUBLIC_KEY' must be set")

DJPADDLE_SUBSCRIBER_MODEL = getattr(
    settings, "DJPADDLE_SUBSCRIBER_MODEL", settings.AUTH_USER_MODEL
)

DJPADDLE_LINK_STALE_SUBSCRIPTIONS = getattr(
    settings, "DJPADDLE_LINK_STALE_SUBSCRIPTIONS", True
)


def get_subscriber_model():
    """
    Attempt to pull settings.DJPADDLE_SUBSCRIBER_MODEL.
    Users have the option of specifying a custom subscriber model via the
    DJPADDLE_SUBSCRIBER_MODEL setting.
    This methods falls back to AUTH_USER_MODEL if DJPADDLE_SUBSCRIBER_MODEL is not set.
    Returns the subscriber model that is active in this project.
    """
    model_name = DJPADDLE_SUBSCRIBER_MODEL

    # Attempt a Django 1.7 app lookup
    try:
        subscriber_model = django_apps.get_model(model_name)
    except ValueError:
        raise ImproperlyConfigured(
            "DJPADDLE_SUBSCRIBER_MODEL must be of the form 'app_label.model_name'."
        )
    except LookupError:
        raise ImproperlyConfigured(
            "DJPADDLE_SUBSCRIBER_MODEL refers to model '{model}' "
            "that has not been installed.".format(model=model_name)
        )

    if (
        "email" not in [field_.name for field_ in subscriber_model._meta.get_fields()]
    ) and not hasattr(subscriber_model, "email"):
        raise ImproperlyConfigured(
            "DJPADDLE_SUBSCRIBER_MODEL must have an email attribute."
        )

    return subscriber_model
