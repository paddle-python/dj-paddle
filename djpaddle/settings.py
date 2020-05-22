from django.apps import apps as django_apps
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from .utils import convert_pubkey_to_rsa

DJPADDLE_API_BASE = getattr(
    settings, "DJPADDLE_API_BASE", "https://vendors.paddle.com/api/2.0/"
)

# can be found at https://vendors.paddle.com/authentication
DJPADDLE_VENDOR_ID = getattr(settings, "DJPADDLE_VENDOR_ID")
if not DJPADDLE_VENDOR_ID:
    raise ImproperlyConfigured("'DJPADDLE_VENDOR_ID' must be set")

# create one at https://vendors.paddle.com/authentication
DJPADDLE_API_KEY = getattr(settings, "DJPADDLE_API_KEY")
if not DJPADDLE_API_KEY:
    raise ImproperlyConfigured("'DJPADDLE_API_KEY' must be set")

# can be found at https://vendors.paddle.com/public-key
DJPADDLE_PUBLIC_KEY = getattr(settings, "DJPADDLE_PUBLIC_KEY")
if not DJPADDLE_PUBLIC_KEY:
    raise ImproperlyConfigured("'DJPADDLE_PUBLIC_KEY' must be set")
try:
    DJPADDLE_KEY = convert_pubkey_to_rsa(DJPADDLE_PUBLIC_KEY)
except Exception as e:
    msg = "failed to convert 'DJPADDLE_PUBLIC_KEY'; original message: {}".format(e)
    raise ImproperlyConfigured(msg)

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

    subscriber_field_names = [
        field_.name for field_ in subscriber_model._meta.get_fields()
    ]
    if "email" not in subscriber_field_names and not hasattr(subscriber_model, "email"):
        raise ImproperlyConfigured(
            "DJPADDLE_SUBSCRIBER_MODEL must have an email attribute."
        )

    return subscriber_model
