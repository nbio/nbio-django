__license__ = "Apache 2.0"
__copyright__ = "Copyright 2008 nb.io"
__author__ = "Randy Reddig - ydnar@nb.io"


from django.template import loader, RequestContext
from django.http import HttpResponse


DEFAULT_CONTENT_TYPE = 'text/html;charset=UTF-8'


def render_template(request, template, dictionary=None):
    if template.__class__ == str or template.__class__ == unicode:
        template = loader.get_template(template)
    context = RequestContext(request, dictionary)
    return template.render(context)
    

def render_response(request, template, dictionary=None, content_type=DEFAULT_CONTENT_TYPE, response_class=HttpResponse):
    return response_class(render_template(request, template, dictionary), content_type)


def build_url(request, is_secure=None, host=None, port=None, path=None, query_string=None):
        if is_secure is None:
            is_secure = request.is_secure()
        host = host or request.META['SERVER_NAME']
        port = port or request.META['SERVER_PORT']
        path = path or request.path
        
        scheme = is_secure and 'https' or 'http'
        if (is_secure and port == '443') or (not is_secure and port == '80') or not port:
            port = ''
        else:
            port = ':' + port
        if query_string:
            url = "%s://%s%s%s?%s" % (scheme, host, port, path, query_string)
        else:
            url = "%s://%s%s%s" % (scheme, host, port, path)
        return url
