
class NodeNotFound(Exception):
    """
    Exception raised when a node is not found in the graph.
    """
    ...

class URLNotFound(Exception):
    """
    Exception raised when a URL is not found for request.
    """
    ...

class HeaderNotFound(Exception):
    """
    Exception raised when a header is not found for request.
    """
    ...

class SOAPStatusException(Exception):
    """
    Exception raised when a SOAP request returns an error.
    """
    ...

class TemplateNotFound(Exception):
    """
    Exception raised when a template is not found.
    """
    ...

class FaultCodeException(Exception):
    """
    Exception raised when a SOAP request returns a fault code.
    """
    def __init__(self, message="", code=None, detail=None):
        super(Exception, self).__init__(message)
        self.message = message
        self.code = code
        self.detail = detail

class NodeNotFoundError(Exception):
    """
    Exception raised when XML element not found
    """
    ...