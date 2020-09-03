from rest_framework_json_api import serializers
from rest.models import User
from django.contrib.auth.forms import PasswordResetForm
from pooling import settings
from allauth.account.utils import setup_user_email
from django.utils.crypto import get_random_string


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'designation', 'phone_number', 'lab_id']

    def create(self, validated_data):
        request = self.context.get('request')
        user = User(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            designation=validated_data['designation'],
            phone_number=validated_data['phone_number'],
            lab_id=validated_data['lab_id'] if request.user.is_staff and 'lab_id' in validated_data.keys() else request.user.lab_id
        )
        user.set_password(get_random_string(length=32))
        user.save()

        setup_user_email(request, user, [])

        # send_email_confirmation(request,user, False)
        reset_form = PasswordResetForm(data={'email': user.email})
        reset_form.is_valid()

        opts = {
            'use_https': request.is_secure(),
            'from_email': settings.DEFAULT_FROM_EMAIL,
            'request': request,
            'subject_template_name': 'registration/set_password_subject.txt',
            'email_template_name': 'registration/set_password.html'
        }
        reset_form.save(**opts)

        return user
