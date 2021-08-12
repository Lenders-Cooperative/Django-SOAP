import requests
import json
import xmltodict
from django_soap.models import (
    SOAPRequestLogger,
    SOAPResponseLogger,
    VERBMAP
)
from collections import OrderedDict
from django.template.loader import get_template, render_to_string
from datetime import datetime, timezone
from django_soap.utils import exceptions
from django.db.models.query import QuerySet


class SoapResult:
    """
    Parses xml response
    """
    def __init__(self, data, status_code):
        if isinstance(data, str):
            self._dict = dict(xmltodict.parse(data))
        elif isinstance(data, dict):
            self._dict = data
        elif isinstance(data, list):
            self._dict = OrderedDict({'Response': data})
        
        self.xml = data
        self.status_code = status_code
        self.value = self._dict

    def _parse_path(self, path: str) -> list:
        return path.split('/')

    def xml_to_json(self):
        return json.dumps(self._dict)
    
    # def has(self, path: str):
    #     try:
    #         self._get(self._dict, self._parse_path(path))
    #     except exceptions.NodeNotFound:
    #         return False
    #     return True
    
    def has(self, value):
        if value in list(self._dict.keys()):
            return True
        return False
    
    def get(self, path, default_value=None):
        try:
            result = self._get(self._dict, self._parse_path(path))
        except exceptions.NodeNotFoundError:
            return default_value
        if isinstance(result, (dict, OrderedDict)):
            return SoapResult(result, self.status_code)
        return result

    def get_list(self, path):
        try:
            result = self._get(self._dict, self._parse_path(path))
        except exceptions.NodeNotFoundError:
            return SoapResult([], self.status_code)
        if isinstance(result, list):
            return SoapResult(result, self.status_code)
        if isinstance(result, (dict, OrderedDict)):
            return SoapResult([result], self.status_code)
        return

    def _find(self, d, key):
        for k, v in d.items():
            if isinstance (v, OrderedDict):
                for found in self._find(v, key):
                    yield found
            if k == key:
                yield v

    def find(self, key):
        return SoapResult(next(self._find(self._dict, key)), self.status_code)

    def get_value(self, path, default_value=False):
        result = self.get(path, default_value)
        if isinstance(result, SoapResult):
            raise exceptions.NotTextFound
        return result

    def _get(self, data, keys):
        try:
            return self._get(data[keys[0]], keys[1:]) if keys else data
        except KeyError:
            raise exceptions.NodeNotFoundError


class SOAPHandlerBase():
    """
    This class is the base class for all the SOAP handlers.
    """
    url = None
    headers = {}

    def __init__(self, *args, **kwargs):
        self.__dict__.update(kwargs)
    
    def _send_request(self, verb: VERBMAP, url: str, data, headers):
        """
        Sends the request to the server.
        """

        if url is None and self.url is None:
            raise exceptions.URLNotFound
        
        if headers is None and (self.headers is {} or self.headers is None):
            raise exceptions.HeaderNotFound
        
        req_log = SOAPRequestLogger.objects.create(
            method=verb.value,
            url=url or self.url,
            headers=str(headers or self.headers),
            body=data,            
        )
        
        r = requests.post(url, data=data, headers=headers)
        response = self._receive_response(req_log, r)
        req_log.request_time_ms = (
            datetime.now(timezone.utc) - req_log.date_sent
        ).microseconds
        req_log.save()

        return response
    
    def _handle_fault_codes(self, response):
        """
        Handles the fault codes.
        """
        if response.status_code != 200:
            error = (
                response
                    .find('soap:Fault')
                    .get_value('faultstring')
            )
            raise Exception(
                f"{error.split(':')[1]} \n"
            )
        return response.status_code

    def _handle_status_codes(self, response):
        """
        Reads status code and returns value, but if it's a 
        bad resoponse, raises an exception.
        """
        if response.status_code < 400:
            return response.status_code

        # SOAP_STATUS_EXCEPTIONS = {
        #     400: 'Bad Request',
        #     401: 'Unauthorized',
        #     403: 'Forbidden',
        #     404: 'Not Found',
        #     405: 'Method Not Allowed',
        #     406: 'Not Acceptable',
        #     500: 'Internal Server Error',
        #     501: 'Not Implemented',
        #     502: 'Bad Gateway',
        #     503: 'Service Unavailable',
        #     504: 'Gateway Timeout'
        # }

        # try:
        #     ...
        # except:
        #     raise exceptions.SOAPStatusException(SOAP_STATUS_EXCEPTIONS[response.status_code])
        
        return response.status_code
    
    def _receive_response(self, request_logger, response) -> SoapResult:
        """
        Updates the SOAPResponseLogger with response info and
        parses the response to a SOAP Result.
        """
        status_code = self._handle_status_codes(response)
    
        SOAPResponseLogger.objects.create(
            request_id=request_logger,
            status=status_code,
            headers=str(response.headers),
            body=str(response.content),
        )

        result = SoapResult(response.text, response.status_code)

        # if status_code != 200:
        #     raise exceptions.SOAPStatusException(
        #         message=result.get(''
        #     )

        return result

    def _prepare_envelope(self, envelope_path: str, envelope_attributes: dict):
        """
        This method prepares the envelope / SOAP request.
        """
        return render_to_string(
            self._get_envelope(envelope_path),
            context=envelope_attributes
        )
    
    def _extend_attributes(self, attributes: dict) -> dict:
        """
        Grabs attributes from class and newely inputed attiibutes.
        The newly inputed attributes overwrite the class attributes.
        """
        
        return (lambda f=self.__dict__.copy(): (f.update(attributes), f)[1])()
    
    def _get_envelope(self, path: str) -> str:
        """
        Looks for the XML file in the templates directory.
        """
        try:
            template = get_template(path)
        except exceptions.TemplateNotFound:
            raise exceptions.TemplateNotFound
        
        return path

    def post(self, envelope_path=None, envelope_attributes=None) -> SoapResult:
        """
        Posts the request to the server.
        """
        # convert all querysets to lists
        for k, v in envelope_attributes.items():
            if isinstance(v, QuerySet):
                envelope_attributes[k] = list(v.values())

        if isinstance(envelope_attributes, QuerySet):
            envelope_attributes = list(envelope_attributes.values())
    
        payload = self._prepare_envelope(
            envelope_path, 
            self._extend_attributes(envelope_attributes or {})
        )

        result = self._send_request(
            VERBMAP.POST,
            envelope_attributes.get('url') or self.url,
            data=payload,
            headers=self.headers
        )
        return result
    
    def get(self, envelope_path=None, envelope_attributes=None) -> SoapResult:
        # NOTE I don't think SOAP does GET requests??
        ...