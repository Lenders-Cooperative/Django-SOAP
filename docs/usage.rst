=====
Usage
=====

To use Django SOAP in a project, add it to your `INSTALLED_APPS`:

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
