from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse, Http404
import django.template.loader
import os.path
import re

RE_MATCH_END_SLASH = re.compile('/$')


def null():
    return


def default(request, **kwargs):
    template_name = 'pages/' + RE_MATCH_END_SLASH.sub('', request.path) + '.html'
    try:
        django.template.loader.get_template(template_name)
        return render_to_response(template_name, {}, context_instance=RequestContext(request))
    except:
        raise Http404
