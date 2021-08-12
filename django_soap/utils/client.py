from django_soap.utils.SOAPHandlerBase import SOAPHandlerBase


class SOAPClient(SOAPHandlerBase):
    """
    Sends request to server and returns response
    """
    def __init__(self, *args, **kwargs):
        super(SOAPClient, self).__init__(*args, **kwargs)
    
    def send_request(self, envelope_path: str, envelope_attributes):
        return self.post(envelope_path, envelope_attributes)
        