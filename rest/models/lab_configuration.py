from django.db import models
from .machine_type import MachineType
from .test_kit import TestKit
from .lab import Lab

class LabConfiguration(models.Model) :
	lab_id = models.ForeignKey(
		Lab,
		on_delete=models.CASCADE
	)
	machine_type = models.ManyToManyField(MachineType)
	test_kit = models.ManyToManyField(TestKit)
	resource_name = 'labConfiguration'
	nsamples = models.SmallIntegerField()
	prevalence = models.FloatField()
	max_poolsize = models.FloatField()
	poolingmatrix_filename = models.TextField(blank=True)