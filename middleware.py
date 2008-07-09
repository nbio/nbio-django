__license__ = "Python"
__copyright__ = "Copyright 2008 PASV"
__author__ = "Randy Reddig - ydnar@shaderlab.com"

import logging
import re
from django.conf import settings
from django.http import HttpResponsePermanentRedirect

RE_MATCH_SLASHES = re.compile('/+|/*$')


class CanonicalMiddleware:
    def process_view(self, request, view_func, view_args, view_kwargs):
        """
        Process the request, and attempt to normalize these components:
        http vs https
        canonical hostname
        port number
        add trailing slash (if required)
        """
        redirect = False
        
        is_secure = bool(request.is_secure)
        if 'secure' in view_kwargs:
            if is_secure != bool(view_kwargs['secure']):
                is_secure = not is_secure
                redirect = True
            del view_kwargs['secure']
        
        host = request.META['SERVER_NAME']
        if 'host' in view_kwargs:
            if host != view_kwargs['host']:
                host = view_kwargs['host']
                redirect = True
            del view_kwargs['host']
        
        port = request.META['SERVER_PORT']
        if 'port' in view_kwargs:
            if port != view_kwargs['port']:
                port = view_kwargs['port']
                redirect = True
            del view_kwargs['port']
        
        path = RE_MATCH_SLASHES.sub('/', request.path)
        if path != request.path:
            redirect = True
        
        if 'path' in view_kwargs:
            if path != view_kwargs['path']:
                path = view_kwargs['path']
                redirect = True
            del view_kwargs['path']
        
        query_string = request.META['QUERY_STRING']
            
        if redirect:
            return self._redirect(request, is_secure, host, port, path, query_string)
    
    def _resolves(self, url):
        try:
            resolve(url)
            return True
        except http.Http404:
            return False

    def _redirect(self, request, is_secure, host, port, path, query_string):
        protocol = is_secure and 'http' or 'https'
        if port == '80' or not port:
            port = ''
        else:
            port = ':' + port
        url = "%s://%s%s%s%s" % (protocol, host, port, path, query_string)
        if settings.DEBUG and request.method == 'POST':
            raise RuntimeError, 'POST requests cannot be redirected.'
        return HttpResponsePermanentRedirect(url)
