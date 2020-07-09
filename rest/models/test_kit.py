from django.db import models

class TestKit(models.Model) :
	name = models.CharField(max_length=50, blank=False, default='')
	description = models.TextField()
	resource_name = 'testKit'


