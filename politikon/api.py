# -*- coding: utf-8 -*-
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status

from django.conf import settings

from .tasks import send_email_task


class ContactAPIView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        sender_name = request.POST.get("name")
        sender_email = request.POST.get("email")
        sender_message = request.POST.get("message")
        message = u"Wiadomość od: {0} \r\n" \
            u"Email: {1} \r\n" \
            u"Treść: {2}"
        send_email_task.delay(
            subject=u"Wiadomość z formularza kontaktowego",
            message=message.format(sender_name, sender_email, sender_message),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.EMAIL_DEFAULT_RECIPIENT]
        )
        return Response(status.HTTP_202_ACCEPTED)
