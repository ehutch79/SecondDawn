from django.conf import settings
from django import http
from django_neve import Http302

class Http302Middleware(object):
    def process_exception(self, request, exception):
        if isinstance(exception, Http302):
            redirect = http.HttpResponseRedirect(exception.args[0])
            return redirect