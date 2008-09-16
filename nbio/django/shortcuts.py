__license__ = "Apache 2.0"
__copyright__ = "Copyright 2008 nb.io"
__author__ = "Randy Reddig - ydnar@nb.io"


from django.template import RequestContext
from django.http import HttpResponse
from django.template import loader


DEFAULT_CONTENT_TYPE = 'text/html;charset=UTF-8'


def render_response(request, template, dictionary=None, content_type=DEFAULT_CONTENT_TYPE):
    if template.__class__ == str:
        template = loader.get_template(template)
    c = RequestContext(request, dictionary)
    return HttpResponse(template.render(c), content_type)
