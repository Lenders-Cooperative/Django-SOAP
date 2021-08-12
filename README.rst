=============================
Django SOAP
=============================

.. image:: https://badge.fury.io/py/django-soap.svg
    :target: https://badge.fury.io/py/django-soap

.. image:: https://travis-ci.org/sal-git/django-soap.svg?branch=master
    :target: https://travis-ci.org/sal-git/django-soap

.. image:: https://codecov.io/gh/sal-git/django-soap/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/sal-git/django-soap

Your project description goes here

Documentation
-------------

The full documentation is at https://django-soap.readthedocs.io.

Quickstart
----------

Install Django SOAP::

    pip install django-soap

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'django_soap.apps.DjangoSoapConfig',
        ...
    )

Add Django SOAP's URL patterns:

.. code-block:: python

    from django_soap import urls as django_soap_urls


    urlpatterns = [
        ...
        url(r'^', include(django_soap_urls)),
        ...
    ]

Features
--------

* TODO

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox


Development commands
---------------------

::

    pip install -r requirements_dev.txt
    invoke -l


Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
