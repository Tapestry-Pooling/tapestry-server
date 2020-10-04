from django.db import models
from .machine_type import MachineType
from .test_kit import TestKit
from .lab import Lab

class LabConfiguration(models.Model) :
	lab_id = models.ForeignKey(
		Lab,
		on_delete=models.CASCADE
	)
	machine_type = models.ManyToManyField(MachineType, default=1)
	test_kit = models.ManyToManyField(TestKit, default=1)
	resource_name = 'labConfiguration'
	nsamples = models.SmallIntegerField(default=64)
	prevalence = models.FloatField(default=7.5)
	max_poolsize = models.FloatField(default=8)
	poolingmatrix_filename = models.TextField(blank=True, default="Tapestry_Pooling_24x64.xlsx")