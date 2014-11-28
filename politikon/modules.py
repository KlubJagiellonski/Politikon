from django.http import HttpResponse
from django.conf import settings

class BasicAuthMiddleware(object):


    def unauthed(self):
        response = HttpResponse("""<html><title>Auth required</title><body>
                                <h1>Authorization Required</h1></body></html>""", mimetype="text/html")
        response['WWW-Authenticate'] = 'Basic realm="Development"'
        response.status_code = 401
        return response

    def process_request(self,request):
        if not request.META.has_key('HTTP_AUTHORIZATION'):

            return self.unauthed()
        else:
            authentication = request.META['HTTP_AUTHORIZATION']
            (authmeth, auth) = authentication.split(' ',1)
            if 'basic' != authmeth.lower():
                return self.unauthed()
            auth = auth.strip().decode('base64')
            username, password = auth.split(':',1)
            if username == settings.BASICAUTH_USERNAME and password == settings.BASICAUTH_PASSWORD:
                return None

            return self.unauthed()
