from django.core.mail import send_mail
from pooling import settings
import logging
from django.template.loader import render_to_string

from django.contrib.sites.models import Site


def new_user_alert(user):
    logger = logging.getLogger(__name__)
    try:
        current_site = Site.objects.get_current()
        subject = render_to_string(
            'registration/signup_subject.txt', {'user': user, 'site_name': current_site.domain})
        html_body = render_to_string(
            'registration/signup_email.html', {'user': user})

        send_mail(
            subject=subject,
            message="",
            html_message=html_body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )
    except Exception as exp:
        print("Error")
        print(exp)
        logger.error('Error sending new user alert to user')
