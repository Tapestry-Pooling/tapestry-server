from django.utils.translation import ugettext_lazy as _

from rest.models import Lab

try:
    from allauth.account import app_settings as allauth_settings
    from allauth.utils import (email_address_exists,
                               get_username_max_length)
    from allauth.account.adapter import get_adapter
    from allauth.account.utils import setup_user_email
except ImportError:
    raise ImportError("allauth needs to be added to INSTALLED_APPS.")

from rest_framework import serializers


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
        # if data['password1'] != data['password2']:
        #     raise serializers.ValidationError(_("The two password fields didn't match."))
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
        # save lab and add reference
        lab = Lab(name=self.cleaned_data['lab'], city=self.cleaned_data['city'])
        lab.save()
        user.lab_id = lab
        user.save()
        setup_user_email(request, user, [])
        return user