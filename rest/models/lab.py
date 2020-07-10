from django.db import models


class Lab(models.Model):
    name = models.CharField(verbose_name = "Lab Name", max_length = 50)
    city = models.CharField(max_length = 50)
    country = models.CharField(max_length = 50)

    def __str__(self):
        return "%s,%s,%s" %(self.name, self.city, self.country)