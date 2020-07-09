from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Lab(models.Model):
    name = models.CharField(verbose_name = "Lab Name", max_length = 50)
    city = models.CharField(max_length = 50)
    country = models.CharField(max_length = 50)

    def __str__(self):
        return "%s,%s,%s" %(self.name, self.city, self.country)


class LabMember(models.Model):
    designation_choices = [("LMN", "Lab Manager"), ("LMB", "Lab Member")]
    name = models.CharField(max_length = 50)
    designation = models.CharField(max_length = 3, choices = designation_choices)
    phone_number = PhoneNumberField()
    email = models.EmailField()
    lab_id = models.ForeignKey(Lab, on_delete = models.CASCADE)

    def __str__(self):
        return self.name


