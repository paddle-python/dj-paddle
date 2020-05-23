Paddle Checkout
===============

Once you have configured dj-paddle you will want to create a checkout page to process orders.


Paddle JS
---------

To use `Paddle checkout <https://developer.paddle.com/guides/how-tos/checkout/paddle-checkout>`_ you need to load in Paddle JS. The easiest way to do this is to include the ``dj-paddle.html`` template on your checkout page.::

    {% include "djpaddle_paddlejs.html" %}


.. note::
    You need to have added the ``djpaddle.context_processors.vendor_id`` template context processor or manually added ``DJPADDLE_VENDOR_ID`` to your context.

If you want to customise the Paddle setup you can manually add PaddleJS and ``Paddle.Setup`` manually with:

.. code-block:: html

    <script src="https://cdn.paddle.com/paddle/paddle.js"></script>
    <script type="text/javascript">
    Paddle.Setup({
        vendor:  {{ DJPADDLE_VENDOR_ID }},
    });
    </script>


Checkout buttons
----------------

You can pass data to Paddle JS by add data attributes to the button. For example to set the users email you can use the ``data-email`` attribute ::

    <a href="#!" class="paddle_button" data-product="{{ paddle_plan.id }}" data-email="{{ user.email }}" >Buy Now!</a>

Additional data can be saved against a order / subsciption using ``passthrough`` as the ``data-passthrough`` attribute ::

    <a href="#!" class="paddle_button" data-product="{{ paddle_plan.id }}" data-email="{{ user.email }}" data-passthrough='{"user_id": {{ user.pk }}, "affiliation": "Acme Corp"}'>Buy Now!</a>

See the `Paddle checkout web sending additional user data page <https://paddle.com/docs/paddle-checkout-web/#sending-additional-user-data>`_  for more information.


Checkout success
----------------

Without writing extra javascript, Paddle's checkout process does not give you any data back when a user completes a purchase. Paddle only sends information to your app via Webhooks. This can mean your app is unaware a purchase has happened until the Webhook is processed.

dj-paddle comes with an extra template which automatically adds very basic checkout data to the ``Checkout`` model via an API request when the checkout process is completed. This is so you don't have to write you own `Post checkout <https://developer.paddle.com/guides/how-tos/checkout/post-checkout>`_ javascript functions.

To use it you need to add the following to your template::

    {% include "djpaddle_post_checkout.html" %}


This is done by automatically registering a Paddle ``successCallback`` onto any html element with the ``paddle_button`` class. This ``successCallback`` does an API request to a dj-paddle endpoint to save Checkout data.

You can then get order details straight away using a ``post_save`` receiver on the ``Checkout`` model and using the `Paddle API getorder <https://developer.paddle.com/api-reference/checkout-api/order-information/getorder>`_ endpoint

.. code-block:: python

    from djpaddle.models import Checkout, Subscription


    def PaddlecheckoutReciever(sender, instance, created, **kwargs):
        if created:
            # Get checkout and subscription data here


    post_save.connect(PaddlecheckoutReciever, sender=Checkout)


Another option is a background task to compare each ``Checkout.id`` against each ``Subscription.checkout_id`` to ensure no Webhooks have been missed.


Other post checkout options
---------------------------

If you want to manually configure what your happens after a checkout has been completed instead of using the ``checkout_push.html`` template please see:

- `Paddles Post checkout page <https://developer.paddle.com/guides/how-tos/checkout/post-checkout>`_
- `Paddles Checkout Events page <https://developer.paddle.com/reference/paddle-js/checkout-events>`_
