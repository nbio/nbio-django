__license__ = "Apache 2.0"
__copyright__ = "Copyright 2008 nb.io"
__author__ = "Randy Reddig - ydnar@nb.io"


from django.template import Library, Node
from django.conf import settings
from nbio.django.shortcuts import build_url


class UrlNode(Node):
    def __init__(self, host=None, path='', allow_override=False):
        self.host = host
        self.path = path
        self.allow_override = allow_override
        if not self.path.startswith('/'):
            self.path = '/' + self.path

    def render(self, context):
        host = self.host
        request = context.get('request')
        if self.allow_override and request and request.META.get('X_OVERRIDE_SERVER_NAME'):
            host = request.META.get('X_OVERRIDE_SERVER_NAME')
        host = host or settings.HOSTS['app']
        return build_url(request, host=host, path=self.path)


def static_url(parser, token):
    try:
        path = ''
        tag_name, path = token.split_contents()
    except ValueError:
        pass
    return UrlNode(host=settings.HOSTS['static'], path=path, allow_override=True)


def app_url(parser, token):
    try:
        path = ''
        tag_name, path = token.split_contents()
    except ValueError:
        pass
    return UrlNode(host=settings.HOSTS['app'], path=path, allow_override=True)


register = Library()
register.tag("static_url", static_url)
register.tag("app_url", app_url)
