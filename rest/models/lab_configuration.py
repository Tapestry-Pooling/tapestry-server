from django.db import models
from .machine_type import MachineType
from .test_kit import TestKit

class LabConfiguration(models.Model) :
	lab_id = models.SmallIntegerField()
	machine_type = models.ManyToManyField(MachineType)
	test_kit = models.ManyToManyField(TestKit)
	resource_name = 'labConfiguration'


