from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from rest.models import User


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = User
        fields = ('email', 'designation', 'phone_number', 'lab_id',)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('email', 'designation', 'phone_number', 'lab_id',)