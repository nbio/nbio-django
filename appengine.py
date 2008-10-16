__license__ = "Apache 2.0"
__copyright__ = "Copyright 2008 nb.io"
__author__ = "Randy Reddig - ydnar@nb.io"


import logging
from django.conf import settings
from django.http import HttpResponseForbidden
from google.appengine.api import users


class AuthMiddleware:
    def process_request(self, request):
        """
        Process the request, and attempt to authenticate using Google's App Engine user API
        """
        user = users.get_current_user()
        if user:
            email = users.get_current_user().email()
            if email not in settings.ALLOWED_USERS:
                return HttpResponseForbidden("User %s does not have permission to view this page." % email)
        return None
