__license__ = "Apache 2.0"
__copyright__ = "Copyright 2008 nb.io"
__author__ = "Randy Reddig - ydnar@nb.io"


import sys
import logging
import re
from time import sleep
from random import randint
from django.conf import settings
from django.http import HttpResponsePermanentRedirect, Http404
from django.core.urlresolvers import resolve
from django.template import loader, TemplateDoesNotExist
from nbio.django.shortcuts import build_url


TEMPLATE_PATH = u'auto'
INDEX_TEMPLATE = u'__index__.html'
RE_SLASHES = re.compile(r'/+')
RE_START_SLASH = re.compile(r'^/+')
RE_END_SLASH = re.compile(r'(?<=.)/$')


request_counter = 0
def increment():
    global request_counter
    request_counter += 1
    return request_counter


class CanonicalMiddleware:
    def process_view(self, request, view_func, view_args, view_kwargs):
        """
        Process the request, and attempt to normalize these components:
        http vs https
        canonical hostname
        port number
        add trailing slash (if required)
        """
        increment()
        
        # test slow ajax
        #sleep(randint(0, 4))
        
        if 'location' in view_kwargs:
            return HttpResponsePermanentRedirect(view_kwargs['location'])
        
        redirect = False
        
        is_secure = request.is_secure()
        if 'secure' in view_kwargs:
            if is_secure != bool(view_kwargs['secure']):
                is_secure = not is_secure
                redirect = True
            del view_kwargs['secure']
        
        host = request.META['SERVER_NAME']
        if 'host' in view_kwargs:
            if host != view_kwargs['host']:
                change = True
                if hasattr(settings, 'HOST_FILTERS'):
                    for filter in settings.HOST_FILTERS:
                        if filter.search(host):
                            change = False
                            request.META['X_OVERRIDE_SERVER_NAME'] = host
                            break
                if change:
                    host = view_kwargs['host']
                    redirect = True
            del view_kwargs['host']
        
        port = request.META['SERVER_PORT']
        if 'port' in view_kwargs:
            if port != view_kwargs['port']:
                port = view_kwargs['port']
                redirect = True
            del view_kwargs['port']
        
        # clean up path
        path = RE_SLASHES.sub(u'/', unicode(request.path))
        
        # redirect to specific path
        if 'path' in view_kwargs:
            if path != view_kwargs['path']:
                path = view_kwargs['path']
            del view_kwargs['path']
        
        # auto view
        else:
            try:
                view_kwargs['template'] = loader.get_template(TEMPLATE_PATH + path)
            except (TemplateDoesNotExist, UnicodeError):
                try:
                    view_kwargs['template'] = loader.get_template(TEMPLATE_PATH + path + u'/' + INDEX_TEMPLATE)
                    if not path.endswith(u'/'):
                        path += '/'
                except (TemplateDoesNotExist, UnicodeError):
                    if not path.endswith(u'/'):
                        if view_func == self._get_view_func(path + u'/'):
                            path += u'/'
        
        # redirect if path has changed
        if path != request.path:
            redirect = True
        
        query_string = request.META['QUERY_STRING']
        
        if redirect:
            url = build_url(request, is_secure, host, port, path, query_string)
            return HttpResponsePermanentRedirect(url)
    
        
    def _get_view_func(self, path):
        try:
            (view_func, view_args, view_kwargs) = resolve(path)
            return view_func
        except Http404:
            return None
