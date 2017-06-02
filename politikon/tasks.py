import binascii
import logging

from celery import shared_task

from django.conf import settings

from .utils import send_mail


logger = logging.getLogger(__name__)


@shared_task
def send_email_task(
    subject, message, from_email, recipient_list, fail_silently=True, attachments=None, cc=None, bcc=None
):
    """
    Common Celery task to send e-mail message to given recipients.
    :param subject: subject of the e-mail
    :param message: e-mail message (in plain text)
    :param from_email: sender address
    :param recipient_list: list of recipient addresses
    :param fail_silently: if True, won't raise exceptions
    :param attachments: optional list of attachments to add to the message
    :param cc: list of cc e-mails
    :param bcc: list of bcc e-mails
    """
    if attachments:
        for attachment in attachments:
            attachment[1] = binascii.a2b_base64(attachment[1])  # decoding

    send_mail(subject, message, from_email, recipient_list, fail_silently, attachments, cc, bcc)
    logger.info(
        u"'events:tasks:send_email_task' finished sending e-mail to '{0}' with subject '{1}'."
        .format('; '.join(recipient_list), subject)
    )
