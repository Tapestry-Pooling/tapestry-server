from django.db import models

class Country(models.Model):
    id = models.AutoField(primary_key=True)

    name = models.CharField('name', max_length=100, blank=False)

    calling_codes = models.CharField('calling_codes', max_length=5, blank=True, null =True)
    alpha_2_code = models.CharField('alpha_2_code', max_length=2, blank=True)
    alpha_3_code = models.CharField('alpha_3_code', max_length=3, blank=True)

    def __str__(self):
        return self.name