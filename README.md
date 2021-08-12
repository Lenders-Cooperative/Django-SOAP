<h1 align="center">Django SOAP</h1>

<div align="center">

[![Status](https://img.shields.io/badge/status-active-success.svg)]()
[![GitHub Issues](https://img.shields.io/github/issues/Lenders-Cooperative/django-password-history)](https://github.com/Lenders-Cooperative/django-password-history/issues)
[![GitHub Pull Requests](https://img.shields.io/github/issues-pr/kylelobo/The-Documentation-Compendium.svg)](https://github.com/Lenders-Cooperative/django-password-history/pulls)
[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)

</div>

---

<p align="center"> A simple and flexible django module to create SOAP requests using Django templates.
    <br> 
</p>

## 📝 Table of Contents

- [About](#about)
- [Getting Started](#getting-started)
- [Running Tests](#running-tests)
- [Usage](#usage)
- [Built Using](#built-using)
- [Authors](#authors)
- [Acknowledgments](#acknowledgements)

## About

A simple and flexible django module to create SOAP requests using Django templates. There's not a lot of magic under the hood as it builds your SOAP envelopes and has useful functions to parse your SOAP response. It also logs your requests and responses to create to aduit the usage. 

## Getting Started

Follow these instructions to install and setup django-soap in your django project.

### Prerequisites

This package relies on `requests`, `xmltodict`, and of course `Django`. 

### Installing

```
pip install django-soap
```

## Running Tests

```
python manage.py test
```

## Usage

In order to use the system you must add djangosoap to your installed apps in your settings.py file.

```python
INSTALLED_APPS = [
    'djangosoap'
]
```

To start using it you'll have to craft your xml and save it in `/templates` 

```xml
<?xml version="1.0" encoding="utf-8"?>
<soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap12="http://www.w3.org/2003/05/soap-envelope">
  <soap12:Body>
    <Add xmlns="http://tempuri.org/">
      <intA>{{ intA }}</intA>
      <intB>{{ intB }}</intB>
    </Add>
  </soap12:Body>
</soap12:Envelope>
```

Now, let's send that template over with some values

```python
from djangosoap.utils.client import SOAPClient


def some_view(request):
    # The variables needed are URL and HEADERS everything 
    # else is extra that you might need for your request
    client = SOAPClient(
        url='http://www.dneonline.com/calculator.asmx?wsdl',
        headers = {'content-type': 'application/soap+xml'}
        username='username',
        password='pass',
    )

    # Load up your crafted XML template from your /templates folder
    # with the values it expects
    response = c.send_request('Add.xml', {'intA': 2, 'intB': 2})

    # The response is of SoapResult and you can get your items like
    value = (
        response
            .get('soap:Envelope')
            .get('soap:Body')
            .get('AddResponse')
            .get_value('AddResult')
    )

```

When you add values to `SOAPClient()` those values will always be in your client object. If you want to update your request with a new url for one request:

```python
response = c.send_request('Sub.xml', {'url': 'http://subtract-url.com', 'intA': 2, 'intB': 2})
```

> Note, if you then call it again it will revert back to the URL you used to create SOAPClient() instance

You can also just send over your quersets to the adapter
```python

dict_of_query_sets = {
    'qs': MyModel.objects.all(),
    'qs2': MyOtherModel.objects.all(),
    'somevalue': 'value'
}

SOAPClient().send_request('envelope.xml', dict_of_query_sets)

# or something like

SOAPClient().send_request('envelope.xml', MyModel.objects.all())

```

The intention is for this package to be very flexible. It comes with a lot of building blocks you might need when sending XML requests. If you find that `SOAPClient()` doesn't meet your needs you can always extend from `SOAPBaseHandler`. Here's an example:

```python
from djangosoap.utils.SOAPHandlerBase import SOAPHandlerBase

class MyOwnSOAPWrapper(SOAPHandlerBase):
    """
    My Custom SOAP Wrapper / Adapter / Class
    """
    def __init__(self, *args, **kwargs):
        important_env_variable = os.environ.get('MY_SUPER_SECRET_KEY')

        super(SOAPClient, self).__init__(*args, **kwargs)
    
    def send_invoice(self, envelope_path, envelope_attributes):
        # Want to do all the heavy lifting parsing in thd Adapter?
        response = self.post(envelope_path, envelope_attributes)

        return (
            response
                .get('soap:Going')
                .get('soap:Down')
                .get('soap:Into')
                .get('soap:A')
                .get('soap:Buring')
                .get('soap:RingOf')
                .get('soap:Fire')
                .get_value('TheValueIWant')
        )
    
    def send_contract(self):
        # Constant variables? Like the template path and environment?
        # Hard code them!
        return self.post('contract_evelope.xml', {'company': 'LendersCooperative'})
    

value = MyOwnSOAPWrapper(url='url', header='{}').send_invoice('invoice.xml', {'stuff': 'stuff'})
response = MyOwnSOAPWrapper().send_contract()
```


## Built Using

- [Django](https://www.djangoproject.com/) - Web Framework
- [Cookiecutter Django Package](https://github.com/pydanny/cookiecutter-djangopackage) - Cookie Cutter Django Package

## Authors
- [Stephen](https://github.com/sal-git) - Working on behalf of Lender's Cooperative


## Acknowledgements

- Inspiration
