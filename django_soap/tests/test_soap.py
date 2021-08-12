from django_soap.utils.SOAPHandlerBase import SOAPHandlerBase
from django_soap.utils.client import SOAPClient
from django_soap.models import SOAPRequestLogger
from django.test import TestCase


class TestSoapBaseHandler(TestCase):
    """
    Tests SOAPHandlerBase class
    """

    TEST_URL = "https://www.dataaccess.com/webservicesserver/NumberConversion.wso"
    TEST_URL_2 = "https://www.dataaccess.com/webservicesserver/NumberConversion.wso"
    ADD_URL = "http://www.dneonline.com/calculator.asmx?wsdl"

    def setUp(self):
        self.soap_handler = SOAPClient()
        self.soap_handler.url = self.TEST_URL
        self.soap_handler.headers = {
            'content-type': 'application/soap+xml',
        }
    
    def test_sending_request(self):
        """
        Tests sending a simple request
        """
        template_path = 'djangosoap/tests/NumberConversion.xml'
        number_to_convert = {
            'ubiNum': 120000
        }
        response = self.soap_handler.send_request(template_path, number_to_convert)
        assert response.status_code == 200 

    def test_update_url_request(self):
        """
        Tests updating the objects default url for one request
        """
        template_path = 'djangosoap/tests/NumberToDollars.xml'
        number_to_convert = {
            'decimal': 240.00,
            'url': self.TEST_URL_2
        }
        response = self.soap_handler.send_request(template_path, number_to_convert)
        assert response.status_code == 200
    
    def test_getting_soap_results(self):
        """
        Tests getting the results from the SOAP request
        """
        template_path = 'djangosoap/tests/NumberConversion.xml'
        number_to_convert = {
            'ubiNum': 120000
        }
        response = self.soap_handler.send_request(template_path, number_to_convert)
        _value = (
                response
                    .get('soap:Envelope')
                    .get('soap:Body')
                    .get('m:NumberToWordsResponse')
                    .get_value('m:NumberToWordsResult')
                )

        assert _value == "one hundred and twenty thousand"
    
    def test_sending_queryset_in_dict(self):
        """
        Tests sending out querysets instead of dictionaries
        """
        template_path = 'djangosoap/tests/Add.xml'

        SOAPRequestLogger.objects.create(
            request_time_ms=200
        )
        SOAPRequestLogger.objects.create(
            request_time_ms=201
        )
    
        name_me_whatever = {
            'qs1': SOAPRequestLogger.objects.order_by('id').first(),
            'qs2': SOAPRequestLogger.objects.order_by('id').last(),
            'url': self.ADD_URL
        }

        response = self.soap_handler.send_request(template_path, name_me_whatever)
        _value = (
                response
                    .get('soap:Envelope')
                    .get('soap:Body')
                    .get('AddResponse')
                    .get_value('AddResult')
                )
        assert _value == '401'
