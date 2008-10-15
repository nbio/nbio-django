__license__ = "Apache 2.0"
__copyright__ = "Copyright 2008 nb.io"
__author__ = "Randy Reddig - ydnar@nb.io"


from django.template import Library, Node
from django.conf import settings
from nbio.django.shortcuts import build_url


class StaticUrlsNode(Node):
    def __init__(self, path):
        self.path = path

    def render(self, context):
        request = context.get('request')
        return build_url(request, host=settings.HOSTS['static'], path=self.path)


def static_url(parser, token):
    try:
        tag_name, path = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires exactly two arguments" % token.contents.split()[0]
    return StaticUrlsNode(path)


register = Library()
register.tag("static_url", static_url)
