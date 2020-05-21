============
Contributing
============

Contributions are welcome, and they are greatly appreciated! Every
little bit helps, and credit will always be given.

You can contribute in many ways:

Types of Contributions
----------------------

Report Bugs
~~~~~~~~~~~

Report bugs at https://github.com/dj-paddle/dj-paddle/issues.

If you are reporting a bug, please include:

* The version of python and Django you're running
* Detailed steps to reproduce the bug.

Fix Bugs
~~~~~~~~

Look through the GitHub issues for bugs. Anything tagged with "bug"
is open to whoever wants to implement it.

Implement Features
~~~~~~~~~~~~~~~~~~

Look through the GitHub issues for features. Anything tagged with "feature"
is open to whoever wants to implement it.

Write Documentation
~~~~~~~~~~~~~~~~~~~

dj-paddle could always use more documentation, whether as part of the
official dj-paddle docs, in docstrings, or even on the web in blog posts,
articles, and such.

If you are adding to dj-paddle's documentation, you can see your changes by
running ``tox -e docs``. The documentation will be generated in the ``docs/``
directory, and you can open ``docs/_build/html/index.html`` in a web browser.

Submit Feedback
~~~~~~~~~~~~~~~

The best way to send feedback is to file an issue at https://github.com/dj-paddle/dj-paddle/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions are welcome :)

Contributor Discussion
~~~~~~~~~~~~~~~~~~~~~~

For questions regarding contributions to dj-paddle, another avenue is our Discord
channel at https://discord.gg/UJY8fcc.

Get Started!
------------

Ready to contribute? Here's how to set up `dj-paddle` for local development.

1. Fork the `dj-paddle` repo on GitHub.
2. Clone your fork locally::

    $ git clone git@github.com:your_name_here/dj-paddle.git

3. Set up your test database. If you're running tests using PostgreSQL::

    $ createdb djpaddle

   or if you want to test vs sqlite (for convenience) or MySQL, they can be selected
   by setting this environment variable::

    $ export DJPADDLE_TEST_DB_VENDOR=sqlite

   or ::

    $ export DJPADDLE_TEST_DB_VENDOR=mysql

   For postgres and mysql, the database host,port,username and password can be set with environment variables, see ``tests/settings.py``

4. Install your local copy into a virtualenv. Assuming you have ``virtualenvwrapper`` installed, this is how you set up your fork for local development::

    $ mkvirtualenv dj-paddle
    $ cd dj-paddle/
    $ python setup.py develop

5. Create a branch for local development::

    $ git checkout -b name-of-your-bugfix-or-feature

   Now you can make your changes locally.

6. When you're done making changes, check that your changes pass the tests.
   A quick test run can be done as follows::

   $ pip install pytest-django pytest-cov
   $ DJPADDLE_TEST_DB_VENDOR=sqlite pytest --reuse-db

   You should also check that the tests pass with other python and Django versions with tox.
   pytest will output both command line and html coverage statistics and will warn you
   if your changes caused code coverage to drop.::

    $ pip install tox
    $ tox

7. If your changes altered the models you may need to generate Django migrations::

    $ DJPADDLE_TEST_DB_VENDOR=sqlite ./manage.py makemigrations

8. Commit your changes and push your branch to GitHub::

    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature

9. Submit a pull request through the GitHub website.

10. Congratulations, you're now a dj-paddle contributor!  Have some <3 from us.


Webhook fixtures
----------------

A fixture for each of the Paddle webhook alerts have been placed at `tests/webhooks/fixtures/<alert_type>.txt`. These fixtures were generated from the output of the Webhook Alert Testing page - https://vendors.paddle.com/webhook-alert-test

Please check the data before using it in a test if it has not been used before. It appears this Paddle features has some bugs and does not always set the sample data to a valid value. For example, according to https://paddle.com/docs/reference-using-webhooks/ the `marketing_consent` field can be either `0` or `1` but the sample data tool sent an empty value.


Django Migration Policy
-----------------------

Migrations are considered a breaking change, so it's not usually not acceptable to add a migration to a stable branch,
it will be a new ``MAJOR.MINOR.0`` release.

A workaround to this in the case that the Paddle API data isn't compatible with out model (eg Paddle is sending ``null`` to a non-null field)
is to implement the ``_manipulate_paddle_object_hook`` classmethod on the model.

Avoid new migrations with non-schema changes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
If a code change produces a migration that doesn't alter the database schema (eg changing ``help_text``) then instead of
adding a new migration you can edit the most recent migration that affects the field in question.

e.g.: https://github.com/dj-paddle/dj-paddle/commit/e2762c38918a90f00c42ecf21187a920bd3a2087

Squash of unreleased migrations on master
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
We aim to keep the number of migration files per release to a minimum per ``MINOR`` release.

In the case where there are several unreleased migrations on master between releases, we squash migrations immediately before release.

So if you're using the master branch with unreleased migrations, ensure you migrate with the squashed migration before upgrading to the next major release.

For more details see the :ref:`squash_migrations` section of the Release process.

Pull Request Guidelines
-----------------------

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.
2. The pull request must not drop code coverage below the current level.
3. If the pull request adds functionality, the docs should be updated. Put
   your new functionality into a function with a docstring.
4. If the pull request makes changes to a model, include Django migrations.
5. The pull request should work for Python 3.6+. Check
   https://travis-ci.org/dj-paddle/dj-paddle/pull_requests
   and make sure that the tests pass for all supported Python versions.
6. Code formatting: Make sure to install ``black`` and ``isort`` with
   ``pip install black isort`` and run ``black .; isort -y``
   at the dj-paddle root to keep a consistent style.
