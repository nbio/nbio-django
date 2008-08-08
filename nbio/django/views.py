__license__ = "Apache 2.0"
__copyright__ = "Copyright 2008 nb.io"
__author__ = "Randy Reddig - ydnar@nb.io"


from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse, Http404
from django.template import loader
import os.path
import re


DEFAULT_CONTENT_TYPE = 'text/html'


def null():
    return


def auto(request, **kwargs):
    try:
        t = kwargs['template']
        c = RequestContext(request)
        return HttpResponse(t.render(c), DEFAULT_CONTENT_TYPE)
    except:
        raise Http404
