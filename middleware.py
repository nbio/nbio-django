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
from django.core.urlresolvers import resolve, set_script_prefix
from django.template import loader, TemplateDoesNotExist
from nbio.django.shortcuts import build_url


TEMPLATE_PATH = u'auto'
RE_SLASHES = re.compile(r'/+')
RE_START_SLASH = re.compile(r'^/+')
RE_START_WWW = re.compile(r'^www\.')
RE_END_SLASH = re.compile(r'(?<=.)/$')
RE_END_HTML = re.compile(r'\.html$')


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
    
    # set script prefix
    set_script_prefix(request.build_absolute_uri('/'))
    
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
    if hasattr(settings, 'STRIP_WWW') and settings.STRIP_WWW:
      host2 = RE_START_WWW.sub('', host)
      if host2 != host:
        host = host2
        redirect = True
    if 'host' in view_kwargs:
      if host != view_kwargs['host']:
        change = True
        if hasattr(settings, 'HOST_FILTERS'):
          for filter in settings.HOST_FILTERS:
            if filter.search(host):
              change = False
              request.META['X_OVERRIDE_SERVER_NAME'] = host
              break
        if hasattr(settings, 'HOST_SUFFIX') and len(settings.HOST_SUFFIX) > 0:
          request.META['X_IMPLICIT_SERVER_NAME'] = host.rsplit(settings.HOST_SUFFIX)[0]
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
        
    # handle slashes
    path = RE_SLASHES.sub(u'/', unicode(request.path))
    path_ends_with_slash = path.endswith(u'/')
    append_slash = hasattr(settings, 'APPEND_SLASH') and settings.APPEND_SLASH
    if not append_slash and path_ends_with_slash and path != u'/':
      path = path[:-1]
    
    # redirect to specific path
    if 'path' in view_kwargs:
      if path != view_kwargs['path']:
        path = view_kwargs['path']
      del view_kwargs['path']
    
    # auto view
    else:
      template_base = TEMPLATE_PATH + path
      
      try:
        view_kwargs['template'] = loader.get_template(template_base)
      except (TemplateDoesNotExist, UnicodeError):
        try:
          view_kwargs['template'] = loader.select_template((template_base + u'.html', template_base + u'/index.html'))
          if append_slash and not path_ends_with_slash:
            path += '/'
        except (TemplateDoesNotExist, UnicodeError):
          if append_slash and not path_ends_with_slash:
            if view_func == self._get_view_func(path + u'/'):
              path += u'/'
      
      if view_kwargs.get('template'):
        path = RE_END_HTML.sub(u'', path)
    
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
