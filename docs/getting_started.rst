Getting Started
===============

Get the distribution
---------------------

Install dj-paddle:

.. code-block:: bash

    pip install dj-paddle

Configuration
--------------

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


djpaddle includes ``vendor_id`` template context processor which adds your vendor ID as ``DJPADDLE_VENDOR_ID`` to each template context

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

First load in PaddleJS and initialise it by including the dj-paddle PaddleJS template in your own template to load PaddleJS::

    {% include "djpaddle_paddlejs.html" %}


Next add a Paddle product or subscription plan into the page context. Below is an example of how to do this using a class based view where ``plan_id`` is passed through as a value from the URL

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


Finally put a ``Buy Now!`` button for the plan subscription you added to the context ::

    <a href="#!" class="paddle_button" data-product="{{ paddle_plan.id }}">Buy Now!</a>


Clicking this button will kick off the Paddle checkout process.
