__license__ = "Apache 2.0"
__copyright__ = "Copyright 2008 nb.io"
__author__ = "Randy Reddig - ydnar@nb.io"


import django.conf
import datetime


counter = 0
def increment():
    global counter
    counter += 1
    return counter


def settings(request):
    return {
        'now': datetime.datetime.now(),
        'settings': django.conf.settings,
        'counter': increment()
    }
