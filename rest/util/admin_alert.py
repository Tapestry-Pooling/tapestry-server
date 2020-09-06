from django.core.mail import send_mail
from pooling import settings
import logging
from django.template.loader import render_to_string


def new_user_alert_email_admin(user):
    logger = logging.getLogger(__name__)
    try:
        subject = render_to_string(
            'registration/new_user_subject.txt', {'user': user})
        html_body = render_to_string(
            'registration/new_user_email.html', {'user': user})

        send_mail(
            subject=subject,
            message="",
            html_message=html_body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=settings.NEW_LAB_ALERT_EMAIL_TO.split(','),
            fail_silently=False,
        )
    except Exception as exp:
        print("Error")
        print(exp)
        logger.error('Error sending new lab alert to admin')
