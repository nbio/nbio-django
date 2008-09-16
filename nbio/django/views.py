__license__ = "Apache 2.0"
__copyright__ = "Copyright 2008 nb.io"
__author__ = "Randy Reddig - ydnar@nb.io"


from nbio.django.shortcuts import render_response
from django.http import Http404


DEFAULT_CONTENT_TYPE = 'text/html'


def null():
    return
    

def auto(request, **kwargs):
    try:
        t = kwargs['template']
    except:
        raise Http404
    return render_response(t)

