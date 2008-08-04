__license__ = "Apache 2.0"
__copyright__ = "Copyright 2008 nb.io"
__author__ = "Randy Reddig - ydnar@nb.io"


import django.conf
import datetime


request_counter = 0
def increment():
    global request_counter
    request_counter += 1
    return request_counter


def settings(request):
    return {
        'now': datetime.datetime.now(),
        'settings': django.conf.settings,
        'request_counter': increment()
    }
