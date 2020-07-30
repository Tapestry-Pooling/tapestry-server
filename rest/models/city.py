from django.db import models
from .country import Country

class City(models.Model):
    id = models.AutoField(primary_key=True)

    name = models.CharField('name', max_length=200, blank=False)

    country = models.ForeignKey(
        Country,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name