from djpaddle.utils import is_valid_webhook


def test_is_valid_webhook_missing_signature():
    assert not is_valid_webhook({})
