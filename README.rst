dj-paddle
=========

|pypi-badge| |travis-badge| |doc-badge| |pyversions-badge|
|license-badge|

Django + Paddle Made Easy

(this project is heavily inspired by `dj-stripe <https://github.com/dj-stripe/dj-stripe/>`_)

Introduction
------------

dj-paddle implements Paddle models (currently Subscription only), for Django.
Set up your webhook and start receiving model updates.
You will then have a copy of all Paddle subscriptions available in Django, no API traffic required!

The full documentation is available at https://dj-paddle.readthedocs.io.

Features
--------

* Django Signals for all incoming webhook events from paddle
* Subscriptions

Requirements
------------

* Django >= 2.1
* Python >= 3.5

Quickstart
----------

Install dj-paddle:

.. code-block:: bash

    pip install dj-paddle

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

djpaddle includes a ``vendor_id`` template context processor which adds your vendor ID as ``DJPADDLE_VENDOR_ID`` to each template context:

.. code-block:: python

    TEMPLATES = [
    {
        ...
        'OPTIONS': {
            ...
            'context_processors': [
                ...
                'djpaddle.context_processors.vendor_id',
                ...
            ]
        }
    }


Run the commands::

    python manage.py migrate

    # fetches all subscription plans from paddle
    python manage.py djpaddle_sync_plans_from_paddle


Paddle Checkout
---------------

Next to setup a `PaddleJS checkout page <https://developer.paddle.com/guides/how-tos/checkout/paddle-checkout>`_

First load in PaddleJS and initialise it by including the dj-paddle PaddleJS template in your own template to load PaddleJS:

.. code-block:: django

    {% include "djpaddle_paddlejs.html" %}


Next add a Paddle product or subscription plan into the page context. Below is an example of how to do this using a class based view where ``plan_id`` is passed through as a value from the URL:

.. code-block:: python

    from django.conf import settings
    from django.views.generic import TemplateView
    from djpaddle.models import Plan


    class Checkout(TemplateView):
        template_name = 'checkout.html'

        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['paddle_plan'] = Plan.objects.get(pk=kwargs['plan_id'])
            # If you have not added 'djpaddle.context_processors.vendor_id' as a template context processors
            context['DJPADDLE_VENDOR_ID'] = settings.DJPADDLE_VENDOR_ID
            return context


Finally put a ``Buy Now!`` button for the plan subscription you added to the context:

.. code-block:: django

    <a href="#!" class="paddle_button" data-product="{{ paddle_plan.id }}">Buy Now!</a>


You can pass data to Paddle JS by add data attributes to the button. For example to set the users email you can use the ``data-email`` attribute:

.. code-block:: django

    <a href="#!" class="paddle_button" data-product="{{ paddle_plan.id }}" data-email="{{ user.email }}" >Buy Now!</a>


A full list of parameters can be found on the `PaddleJS parameters page <https://developer.paddle.com/webhook-reference/intro>`_


For more information about options on what to do after a successful checkout please see our  `Checkout success documentation <https://dj-paddle.readthedocs.io/en/latest/paddle_checkout.html#checkout-success>`_


Subscription model
------------------

You can override the model that subscriptions are attached to using the ``DJPADDLE_SUBSCRIBER_MODEL`` setting. This setting must use the string model reference in the style 'app_label.ModelName'.

The model chosen must have an ``email`` field.

.. code-block:: python

    # Defaults to AUTH_USER_MODEL
    DJPADDLE_SUBSCRIBER_MODEL = 'myapp.MyModel'

**Warning**: To use this setting you must have already created and ran the initial migration for the app/model before adding ``djpadding`` to ``INSTALLED_APPS``.

Reporting Security Issues
-------------------------

Please do not report security issues in public, but email the authors directly.

.. |pypi-badge| image:: https://img.shields.io/pypi/v/dj-paddle.svg
    :target: https://pypi.python.org/pypi/dj-paddle/
    :alt: PyPI

.. |travis-badge| image:: https://travis-ci.org/paddle-python/dj-paddle.svg?branch=master
    :target: https://travis-ci.org/paddle-python/dj-paddle
    :alt: Travis

.. |doc-badge| image:: https://readthedocs.org/projects/dj-paddle/badge/?version=latest
    :target: http://dj-paddle.readthedocs.io/en/latest/
    :alt: Documentation

.. |pyversions-badge| image:: https://img.shields.io/pypi/pyversions/dj-paddle.svg
    :target: https://pypi.python.org/pypi/dj-paddle/
    :alt: Supported Python versions

.. |license-badge| image:: https://img.shields.io/github/license/paddle-python/dj-paddle
    :target: https://github.com/paddle-python/dj-paddle/blob/master/LICENSE
    :alt: License
