__license__ = "Python"
__copyright__ = "Copyright 2008 PASV"
__author__ = "Randy Reddig - ydnar@shaderlab.com"

import django.conf
import datetime


def settings(request):
    return {
        'now': datetime.datetime.now(),
        'settings': django.conf.settings,
    }
