import pytest
from django.core.exceptions import ImproperlyConfigured


def test_missing_djpaddle_vendor_id(settings):
    settings.DJPADDLE_VENDOR_ID = None
    from djpaddle import settings
    from importlib import reload

    with pytest.raises(ImproperlyConfigured):
        reload(settings)


def test_missing_djpaddle_api_key(settings):
    settings.DJPADDLE_API_KEY = None
    from djpaddle import settings
    from importlib import reload

    with pytest.raises(ImproperlyConfigured):
        reload(settings)


def test_missing_djpaddle_public_key(settings):
    settings.DJPADDLE_PUBLIC_KEY = None
    from djpaddle import settings
    from importlib import reload

    with pytest.raises(ImproperlyConfigured):
        reload(settings)


def test_invalid_djpaddle_public_key(settings):
    settings.DJPADDLE_PUBLIC_KEY = 123
    from djpaddle import settings
    from importlib import reload

    with pytest.raises(ImproperlyConfigured):
        reload(settings)


def test_missing_sandbox(settings):
    from djpaddle import settings
    from importlib import reload

    reload(settings)
    from djpaddle.settings import DJPADDLE_SANDBOX
    assert DJPADDLE_SANDBOX is False


def test_invalid_sandbox(settings):
    settings.DJPADDLE_SANDBOX = 'NOT-TRUE-OR-FALSE'
    from djpaddle import settings
    from importlib import reload

    with pytest.raises(ImproperlyConfigured) as error:
        reload(settings)
    assert error.match("'DJPADDLE_SANDBOX' must be a boolean")


def test_djpaddle_subscriber_model_invalid_name(settings):
    settings.DJPADDLE_SUBSCRIBER_MODEL = "fakemodel"
    from djpaddle import settings
    from importlib import reload

    reload(settings)
    from djpaddle.settings import get_subscriber_model

    with pytest.raises(ImproperlyConfigured):
        get_subscriber_model()


def test_djpaddle_subscriber_model_does_not_exist(settings):
    settings.DJPADDLE_SUBSCRIBER_MODEL = "app_label.model_name"
    from djpaddle import settings
    from importlib import reload

    reload(settings)
    from djpaddle.settings import get_subscriber_model

    with pytest.raises(ImproperlyConfigured):
        get_subscriber_model()
