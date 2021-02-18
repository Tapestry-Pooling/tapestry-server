from django.core.mail import send_mail
from pooling import settings
import logging
from django.template.loader import render_to_string
from django.contrib.sites.models import Site

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



def test_review_alert_email_admin(test_id, positive, inconclusive):
    logger = logging.getLogger(__name__)
    try:
        current_site = Site.objects.get_current()
        user = {"first_name":"Admin"}
        html_body = render_to_string(
            'registration/admin_results_email.html',
            {
                'user': user,
                "testID" : test_id,
                'positive': positive,
                "inconclusive": inconclusive,
                "domain": current_site.domain,
                "protocol": "https"
            }
        )
        send_mail(
            subject='Results of the test with id {} are Ready!'.format(test_id),
            message="",
            html_message=html_body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=settings.NEW_LAB_ALERT_EMAIL_TO.split(','),
            fail_silently=False,
        )
    except Exception as exp:
        logger.error('Error sending test result alert to admin',exp)

def file_error_alert_email_admin(filename, error_status):
    logger = logging.getLogger(__name__)
    try:
        send_mail(
            'File Upload Error',
            'Please review the file: %d with' % filename ,
            'Error: %d', error_status,
            settings.DEFAULT_FROM_EMAIL,
            settings.NEW_LAB_ALERT_EMAIL_TO.split(','),
            fail_silently=False
        )
    except Exception as exp:
        logger.error('Error sending test review alert to admin',exp)
