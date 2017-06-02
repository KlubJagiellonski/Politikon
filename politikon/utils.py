from django.core.mail import EmailMessage


def send_mail(subject, message, from_email, recipient_list, fail_silently=True, attachments=None, cc=None, bcc=None):
    """
    Sends e-mail message similarly to django.core.mail.send_mail but with possibility to add attachments.
    :param subject: subject of the e-mail
    :param message: e-mail message (in plain text)
    :param from_email: sender address
    :param recipient_list: list of recipient addresses
    :param fail_silently: if True, won't raise exceptions
    :param attachments: list of email.MIMEBase.MIMEBase instances or (filename, content, mimetype) tuples
                        where mimetype is optional
    :param cc: list of cc e-mails
    :param bcc: list of bcc e-mails
    :return: number of messages sent
    """
    email = EmailMessage(
        subject=subject,
        body=message,
        from_email=from_email,
        to=recipient_list,
        cc=cc,
        bcc=bcc
    )
    if attachments:
        for attachment in attachments:
            if hasattr(attachment, '__iter__'):
                email.attach(*attachment)
            else:
                email.attach(attachment)

    return email.send(fail_silently=fail_silently)
