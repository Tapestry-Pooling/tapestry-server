from django.utils.translation import ugettext_lazy as _

from rest.models import Lab
from pooling import settings
from django.contrib.auth.forms import PasswordResetForm
try:
    from allauth.account import app_settings as allauth_settings
    from allauth.utils import (email_address_exists,
                               get_username_max_length)
    from allauth.account.adapter import get_adapter
    from allauth.account.utils import setup_user_email
except ImportError:
    raise ImportError("allauth needs to be added to INSTALLED_APPS.")

from rest_framework import serializers
from rest.util.admin_alert import new_user_alert_email_admin
from django.utils.crypto import get_random_string

class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(required=allauth_settings.EMAIL_REQUIRED)
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    lab = serializers.CharField()
    city = serializers.CharField()

    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if allauth_settings.UNIQUE_EMAIL:
            if email and email_address_exists(email):
                raise serializers.ValidationError(
                    _("A user is already registered with this e-mail address."))
        return email

    def validate_first_name(self, first_name):
        return first_name

    def validate_last_name(self, last_name):
        return last_name

    def validate_lab(self, lab):
        return lab

    def validate_city(self, city):
        return city

    def validate(self, data):
        return data


    def get_cleaned_data(self):
        return {
            'email': self.validated_data.get('email', ''),
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
            'lab': self.validated_data.get('lab', ''),
            'city': self.validated_data.get('city', '')
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        # save lab, add reference and set user inactive
        lab = Lab(name=self.cleaned_data['lab'], city=self.cleaned_data['city'])
        lab.save()
        user.lab_id = lab
        user.is_active = False
        user.password = get_random_string(length=32)
        user.save()
        setup_user_email(request, user, [])

        # Alert the admin about the new user.
        new_user_alert_email_admin(lab.name)

        return user