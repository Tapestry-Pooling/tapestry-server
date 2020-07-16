from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _

from rest.managers import UserManager
from phonenumber_field.modelfields import PhoneNumberField
from rest.models import Lab


class User(AbstractUser):
    designation_choices = [("LMN", "Lab Manager"), ("LMB", "Lab Member")]
    username = None
    email = models.EmailField(_('email address'), unique=True)
    designation = models.CharField(_('designation'), max_length=3, choices=designation_choices, blank=True)
    phone_number = PhoneNumberField(_('phone number'), blank=True)
    lab_id = models.ForeignKey(Lab, on_delete=models.CASCADE, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email