from django.db import models


class PaddleCurrencyCodeField(models.CharField):
    """
    A field used to store a three-letter currency code (eg. USD, EUR, ...)
    """

    def __init__(self, *args, **kwargs):
        defaults = {"max_length": 3, "help_text": "Three-letter ISO currency code"}
        defaults.update(kwargs)
        super().__init__(*args, **defaults)
