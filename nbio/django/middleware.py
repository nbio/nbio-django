__license__ = "Apache 2.0"
__copyright__ = "Copyright 2008 nb.io"
__author__ = "Randy Reddig - ydnar@nb.io"


import logging
import re
from django.conf import settings
from django.http import HttpResponsePermanentRedirect, Http404
from django.core.urlresolvers import resolve
from django.template import loader



TEMPLATE_PATH = 'auto'
INDEX_TEMPLATE = '__index__.html'
RE_MATCH_SLASHES = re.compile(r'/+')
RE_MATCH_END_SLASH = re.compile(r'(?<=.)/$')


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
        
        if 'location' in view_kwargs:
            return HttpResponsePermanentRedirect(view_kwargs['location'])
        
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
        
        # clean up path
        path = RE_MATCH_SLASHES.sub('/', request.path)
        
        # redirect to specific path
        if 'path' in view_kwargs:
            if path != view_kwargs['path']:
                path = view_kwargs['path']
            del view_kwargs['path']
        
        # auto view
        else:
            try:
                view_kwargs['template'] = loader.get_template(TEMPLATE_PATH + path)
            except:
                try:
                    view_kwargs['template'] = loader.get_template(TEMPLATE_PATH + path + '/' + INDEX_TEMPLATE)
                    if not path.endswith('/'):
                        path += '/'
                except:
                    if not path.endswith('/'):
                        if view_func == self._get_view_func(path + '/'):
                            path += '/'
        
        # redirect if path has changed
        if path != request.path:
            redirect = True
        
        query_string = request.META['QUERY_STRING']
            
        if redirect:
            return self._redirect(request, is_secure, host, port, path, query_string)
    
        
    def _get_view_func(self, path):
        try:
            (view_func, view_args, view_kwargs) = resolve(path)
            return view_func
        except Http404:
            return None
            
    
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
