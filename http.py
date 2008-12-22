from __future__ import absolute_import
from django.http import HttpResponse
from django.utils import simplejson


__license__ = "Apache 2.0"
__copyright__ = "Copyright 2008 nb.io"
__author__ = "Randy Reddig - ydnar@nb.io"


JSON_CONTENT_TYPE = "text/javascript+json"
CSS_CONTENT_TYPE = "text/css"


class JSONHttpResponse(HttpResponse):
    def __init__(self, content):
        super(JSONHttpResponse, self).__init__(simplejson.dumps(content), JSON_CONTENT_TYPE)
    

class CSSHttpResponse(HttpResponse):
    def __init__(self, content):
        import csshttprequest
        super(CSSHttpResponse, self).__init__(csshttprequest.encode(content), CSS_CONTENT_TYPE)


class JSONCSSHttpResponse(CSSHttpResponse):
    def __init__(self, content):
        super(JSONCSSHttpResponse, self).__init__(simplejson.dumps(content))
