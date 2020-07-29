from django.core.mail import send_mail
from pooling import settings
import logging


def new_user_alert_email_admin(lab_name):
    logger = logging.getLogger(__name__)
    try:
        send_mail(
            'New Lab Registered', 
            'Please verify the new lab : ' + lab_name , 
            settings.DEFAULT_FROM_EMAIL, 
            settings.NEW_LAB_ALERT_EMAIL_TO.split(','), 
            fail_silently=False
        )
    except Exception as exp:
        logger.error('Error sending new lab alert to admin',exp)
