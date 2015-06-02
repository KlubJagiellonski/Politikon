from django.http import HttpResponsePermanentRedirect
from django.contrib.auth import logout as auth_logout


def login(request):
    return HttpResponsePermanentRedirect('/')

def logout(request):
    auth_logout(request)
    return HttpResponsePermanentRedirect('/')
