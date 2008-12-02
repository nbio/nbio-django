__license__ = "Apache 2.0"
__copyright__ = "Copyright 2008 nb.io"
__author__ = "Randy Reddig - ydnar@nb.io"


from django.http import HttpResponse
from django.utils import simplejson


JSON_CONTENT_TYPE = "application/javascript+json"
CSS_CONTENT_TYPE = "text/css"


class JSONHttpResponse(HttpResponse):
    def __init__(self, content):
        super(JSONHttpResponse, self).__init__(simplejson.dumps(content), JSON_CONTENT_TYPE)
    

class CSSHttpResponse(HttpResponse):
    def __init__(self, content):
        from nbio.csshttprequest import encode
        super(CSSHttpResponse, self).__init__(encode(content), CSS_CONTENT_TYPE)


class JSONCSSHttpResponse(CSSHttpResponse):
    def __init__(self, content):
        super(JSONCSSHttpResponse, self).__init__(simplejson.dumps(content))
