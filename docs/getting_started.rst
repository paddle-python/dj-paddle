Getting Started
===============

Get the distribution
---------------------

Install dj-paddle:

.. code-block:: bash

    pip install dj-paddle

Configuration
---------------

Add ``djpaddle`` to your ``INSTALLED_APPS``:

.. code-block:: python

    INSTALLED_APPS =(
        ...
        "djpaddle",
        ...
    )

Add to urls.py:

.. code-block:: python

    path("paddle/", include("djpaddle.urls", namespace="djpaddle")),

Tell paddle about the webhook (paddle webhook docs can be found `here <https://developer.paddle.com/webhook-reference/intro>`_) using the full URL of your endpoint from the urls.py step above (e.g. ``https://example.com/paddle/webhook/``).

Add your paddle keys and set the operating mode:

.. code-block:: python

    # can be found at https://vendors.paddle.com/authentication
    DJPADDLE_VENDOR_ID = '<your-vendor-id>'

    # create one at https://vendors.paddle.com/authentication
    DJPADDLE_API_KEY = '<your-api-key>'

    # can be found at https://vendors.paddle.com/public-key
    DJPADDLE_PUBLIC_KEY = '<your-public-key>'

Run the commands::

    python manage.py migrate

    # fetches all subscription plans from paddle
    python manage.py djpaddle_sync_plans_from_paddle
