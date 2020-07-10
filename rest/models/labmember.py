from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from rest.models import Lab


class LabMember(models.Model):
    designation_choices = [("LMN", "Lab Manager"), ("LMB", "Lab Member")]
    name = models.CharField(max_length = 50)
    designation = models.CharField(max_length = 3, choices = designation_choices)
    phone_number = PhoneNumberField()
    email = models.EmailField()
    lab_id = models.ForeignKey(Lab, on_delete = models.CASCADE)

    def __str__(self):
        return self.name