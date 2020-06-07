Paddle Checkout
===============

Once you have configured dj-paddle you will want to create a checkout page to process orders.


Paddle JS
---------

To use `Paddle checkout <https://developer.paddle.com/guides/how-tos/checkout/paddle-checkout>`_ you need to load in Paddle JS. The easiest way to do this is to include the ``dj-paddle.html`` template on your checkout page.::

    {% include "djpaddle_paddlejs.html" %}


.. note::
    You need to have added the ``djpaddle.context_processors.vendor_id`` template context processor or manually add ``DJPADDLE_VENDOR_ID`` to your context.

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


This is done by automatically registering a Paddle ``successCallback`` onto any HTML element with the ``paddle_button`` class. ```successCallback`` then does an API request to a dj-paddle endpoint to save Checkout data.


Redirect after checkout
^^^^^^^^^^^^^^^^^^^^^^^

If you want to redirect the user after the checkout process is complete while using ``djpaddle_post_checkout.html`` you can add a  context variable called ``djpaddle_checkout_success_redirect``.

This will then redirect the user after the checkout data has been saved. The redirect will also include a checkout query parameter ``?checkout={checkout_id}`` so you can look up the checkout information on the redirected page.


Post-Checkout Order Information
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Once the user has completed an order, you will probably want to display some kind of success message to you user with some information about the order. The best way to do this is redirecting the user to a success page using the ``djpaddle_checkout_success_redirect`` context variable above.

In the redirect view you can then get the basic order information from Paddle

.. code-block:: python
    from django.http import Http404
    from django.views.generic TemplateView
    from paddle import PaddleClient, PaddleException


    class CheckoutSuccess(TemplateView):
        template_name = 'checkout_success.html'

        def get(self, request, *args, **kwargs):
            context = self.get_context_data(**kwargs)
            checkout_id = request.GET['checkout']
            paddle = PaddleClient()
            try:
                order_details = paddle.get_order_details(checkout_id=checkout_id)
            except PaddleException:
                raise Http404()
            context['order_details'] = order_details
            return self.render_to_response(context)


.. note::
    As `Paddle Post Checkout Order Information <https://developer.paddle.com/api-reference/checkout-api/order-information/getorder>`_ states, order processing may take a few seconds after the transaction to complete. It's best to wait for the created / succeeded webhook to be processed before actually creating updating your model(s).

.. note::
    dj-paddle does not yet support one-off purchases and does not do anything with ``payment_succeeded`` webhooks. This means there is currently no signal for one of purchases.


To get notified as soon as the ``subscription_created`` Webhook has been processed by dj-paddle you can listen to a ``post_save`` signal on the ``Subscription`` model.

.. code-block:: python

    from djpaddle.models import Subscription


    def paddle_subscription_reciever(sender, instance, created, **kwargs):
        if created:
            ...

    post_save.connect(paddle_subscription_reciever, sender=Subscription)



Keeping checkout information in sync
------------------------------------

Due to Paddles checkout flow, it could be possible to miss checkout data and your system not to be in sync with Paddle. Because of this, you may want to ensure your data is in sync with Paddle.


Using the dj-paddle checkout model
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you have been using the ``djpaddle_post_checkout.html`` template you should have a record of each successful checkout in the djpaddle Checkout model. This model can then be used to compare each ``Checkout.id`` against each ``Subscription.checkout_id`` to ensure no Webhooks have been missed.

More info and management command coming soon


Using Paddle's Webhook history
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Retrieving past events and alerts that Paddle has sent via webhooks using the `Get Webhook History API <https://developer.paddle.com/api-reference/alert-api/webhooks/webhooks>`_. They should be replayed in the order they were created.

More info and management command coming soon



Other Paddle post checkout options
----------------------------------

If you want to manually configure what happens after a checkout has been completed instead of using the ``checkout_push.html`` template please see:

- `Order Information <https://paddle.com/docs/paddlejs-order-information/>`_
- `Paddles Post checkout page <https://developer.paddle.com/guides/how-tos/checkout/post-checkout>`_
- `Paddles Checkout Events page <https://developer.paddle.com/reference/paddle-js/checkout-events>`_

.. note::
    - Subscriptions currently do not have an option within Paddle to set a redirect URL via the seller dashboard
    - For normal products, using the ``successCallback`` or ``data-success-callback`` will override any success redirect set in your Seller Dashboard. This includes using the ``djpaddle_post_checkout`` template above
    - When redirecting using the ``data-success`` attribute (`mentioned here <https://paddle.com/support/how-can-i-redirect-buyers-upon-completing-the-checkout/>`_), the redirect URL will **NOT** receive a checkout query parameter (``checkout={checkout_hash}``). Because of this, it is not advised to use this as the redirect provides no information about the checkout that has just been completed
    - If you still want to use ``data-success`` ensure the value is set to the full URL of your application using ``request.build_absolute_uri()``
