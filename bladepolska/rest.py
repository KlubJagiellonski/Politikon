from bladepolska.http import HttpResponseUnauthorized
from django.utils.functional import wraps

def rest_api_login_required(view):
    @wraps(view)
    def inner(request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseUnauthorized()

        return view(request, *args, **kwargs)

    return inner
