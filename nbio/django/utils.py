__license__ = "Apache 2.0"
__copyright__ = "Copyright 2008 nb.io"
__author__ = "Randy Reddig - ydnar@nb.io"


import urllib
from django.utils.encoding import smart_str
from django.core.urlresolvers import reverse


def iri_to_uri(iri):
    """
    Convert an Internationalized Resource Identifier (IRI) portion to a URI
    portion that is suitable for inclusion in a URL.

    This is the algorithm from section 3.1 of RFC 3987.  However, since we are
    assuming input is either UTF-8 or unicode already, we can simplify things a
    little from the full method.

    Returns an ASCII string containing the encoded result.
    
    Slightly more liberal than the Django built-in
    """
    # The list of safe characters here is constructed from the printable ASCII
    # characters that are not explicitly excluded by the list at the end of
    # section 3.1 of RFC 3987.
    # added '@' to allowed set
    if iri is None:
        return iri
    return urllib.quote(smart_str(iri), safe='/#%[]=:;$&()+,!?*@')


def reverse_slash(viewname, urlconf=None, args=None, kwargs=None, prefix=None):
    url = reverse(viewname, urlconf=urlconf, args=args, kwargs=kwargs, prefix=prefix)
    if not url.endswith('/'):
        url = url + '/'
    return url
