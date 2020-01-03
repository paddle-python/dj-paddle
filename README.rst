dj-paddle
=============================

|pypi-badge| |travis-badge| |doc-badge| |pyversions-badge|
|license-badge|

Django + Paddle Made Easy

(this project is heavily inspired by `dj-stripe <https://github.com/dj-stripe/dj-stripe/>`_)

Introduction
------------------------

dj-paddle implements Paddle models (currently Subscription only), for Django.
Set up your webhook and start receiving model updates.
You will then have a copy of all Paddle subscriptions available in Django, no API traffic required!

The full documentation is available at https://dj-paddle.readthedocs.org.

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

Run the commands::

    python manage.py migrate


Reporting Security Issues
-------------------------

Please do not report security issues in public, but email the authors directly.


.. |pypi-badge| image:: https://img.shields.io/pypi/v/dj-paddle.svg
    :target: https://pypi.python.org/pypi/dj-paddle/
    :alt: PyPI

.. |travis-badge| image:: https://travis-ci.org/dj-paddle/dj-paddle.svg?branch=master
    :target: https://travis-ci.org/dj-paddle/dj-paddle
    :alt: Travis

.. |doc-badge| image:: https://readthedocs.org/projects/dj-paddle/badge/?version=latest
    :target: http://dj-paddle.readthedocs.io/en/latest/
    :alt: Documentation

.. |pyversions-badge| image:: https://img.shields.io/pypi/pyversions/dj-paddle.svg
    :target: https://pypi.python.org/pypi/dj-paddle/
    :alt: Supported Python versions

.. |license-badge| image:: https://img.shields.io/github/license/dj-paddle/dj-paddle
    :target: https://github.com/dj-paddle/dj-paddle/blob/master/LICENSE
    :alt: License
