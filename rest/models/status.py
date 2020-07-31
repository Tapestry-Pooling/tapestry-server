from django.db import models

class Status(models.Model):
    name = models.CharField(max_length = 50)

    class Meta:
        verbose_name_plural = 'Statuses'

    def __str__(self):
        return self.name