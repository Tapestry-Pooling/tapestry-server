from django.db import models

class Status(models.Model):
    name = models.CharField(max_length = 50)