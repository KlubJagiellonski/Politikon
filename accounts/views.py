from django.http import HttpResponsePermanentRedirect
from django.contrib.auth import logout as auth_logout
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView

