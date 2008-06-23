__license__ = "Python"
__copyright__ = "Copyright 2008 PASV"
__author__ = "Randy Reddig - ydnar@shaderlab.com"

import django.conf


def settings(request):
    return {
        'settings': django.conf.settings,
    }
