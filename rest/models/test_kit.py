from django.db import models
from django.contrib.postgres.fields import ArrayField

class TestKit(models.Model) :
	name = models.CharField(max_length=80, blank=False, default='')
	kit_maker = models.CharField(max_length=50, blank=False, default='')
	gene_type = ArrayField(base_field=models.CharField(max_length=10), size=6)
	test_type = models.CharField(max_length=20, blank=False, default='')
	resource_name = 'testKit'
