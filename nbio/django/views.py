__license__ = "Apache 2.0"
__copyright__ = "Copyright 2008 nb.io"
__author__ = "Randy Reddig - ydnar@nb.io"


from nbio.django.shortcuts import render_response
from django import http


DEFAULT_CONTENT_TYPE = 'text/html'


def null():
    return
    

def auto(request, **kwargs):
    try:
        t = kwargs['template']
    except KeyError:
        raise http.Http404
    return render_response(request, t)


def page_not_found(request, **kwargs):
    t = kwargs.get('template', '404.html')
    return render_response(request, t, response_class=http.HttpResponseNotFound)


def server_error(request, **kwargs):
    t = kwargs.get('template', '500.html')
    return render_response(request, t, response_class=http.HttpResponseServerError)
