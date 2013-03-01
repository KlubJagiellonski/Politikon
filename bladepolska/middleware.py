# Copyright (C) 2011 by Blade Polska s.c.
# Full rights belong to Tomek Kopczuk (@tkopczuk).
# www.askthepony.com
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import cProfile
from datetime import datetime
from django.contrib.auth.middleware import AuthenticationMiddleware
from django.contrib.messages.middleware import MessageMiddleware
from django.contrib.sessions.middleware import SessionMiddleware
from django.middleware.csrf import CsrfViewMiddleware
import os
import StringIO

isAPIRequest = lambda request: request.path_info[0:5] == '/api/'


# Session performance
class SessionMiddlewareOmitApi(SessionMiddleware):
    def process_request(self, request):
        if isAPIRequest(request):
            return
        super(SessionMiddlewareOmitApi, self).process_request(request)

    def process_response(self, request, response):
        if isAPIRequest(request):
            return response
        return super(SessionMiddlewareOmitApi, self).process_response(request, response)


class AuthenticationMiddlewareOmitApi(AuthenticationMiddleware):
    def process_request(self, request):
        if hasattr(request, 'user'):
            return
        if isAPIRequest(request):
            return
        super(AuthenticationMiddlewareOmitApi, self).process_request(request)


class MessageMiddlewareOmitApi(MessageMiddleware):
    def process_request(self, request):
        if isAPIRequest(request):
            return
        super(MessageMiddlewareOmitApi, self).process_request(request)

    def process_response(self, request, response):
        if isAPIRequest(request):
            return response
        return super(MessageMiddlewareOmitApi, self).process_response(request, response)


class CsrfViewMiddlewareOmitApi(CsrfViewMiddleware):
    def process_view(self, request, callback, callback_args, callback_kwargs):
        if isAPIRequest(request):
            return
        super(CsrfViewMiddlewareOmitApi, self).process_view(request, callback, callback_args, callback_kwargs)

    def process_response(self, request, response):
        if isAPIRequest(request):
            return response
        return super(CsrfViewMiddlewareOmitApi, self).process_response(request, response)


# Instrumentation
class InstrumentMiddleware(object):
    def process_request(self, request):
        if 'profile' in request.REQUEST:
            request.profiler = cProfile.Profile()
            request.profiler.enable()

    def process_response(self, request, response):
        if hasattr(request, 'profiler'):
            request.profiler.disable()
            stamp = (request.META['REMOTE_ADDR'], datetime.now())
            request.profiler.dump_stats('/tmp/%s-%s.pro' % stamp)
            import pstats
            stream = StringIO.StringIO()
            stats = pstats.Stats('/tmp/%s-%s.pro' % stamp, stream=stream)
#            stats.strip_dirs()
            stats.sort_stats('time')
            stats.print_stats(12)
            stats.print_callers(12)
            stats.print_callees(12)
            os.remove('/tmp/%s-%s.pro' % stamp)
            #response._container[0] += "<pre>"+stream.getvalue()+"</pre>"
            print stream.getvalue()
            stream.close()

            from django.db import connection
            for query in connection.queries:
                print query['time'], query['sql']
            print len(connection.queries), 'queries, overall time', "%.3f" % sum([float(query['time']) for query in connection.queries])
        return response
