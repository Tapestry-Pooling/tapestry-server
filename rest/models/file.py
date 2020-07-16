from django.db import models

class File(models.Model):
    path = models.CharField(max_length = 100)