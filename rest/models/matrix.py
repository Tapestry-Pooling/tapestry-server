from django.db import models
from django.contrib.postgres import fields

class Matrix(models.Model):
    kirkman_matrix = fields.JSONField()