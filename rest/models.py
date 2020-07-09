from django.db import models

# Create your models here.

class MachineType(models.Model) :
	name = models.CharField(max_length=60, blank=False, default='PCR machine')
	no_of_wells = models.SmallIntegerField()
	plate_x = models.SmallIntegerField(default=12)
	plate_y = models.SmallIntegerField(default=8)
	resource_name = 'machineType'

class TestKit(models.Model) :
	name = models.CharField(max_length=50, blank=False, default='')
	description = models.TextField()
	resource_name = 'testKit'

class LabConfiguration(models.Model) :
	lab_id = models.SmallIntegerField()
	machine_type = models.ManyToManyField(MachineType)
	test_kit = models.ManyToManyField(TestKit)
	resource_name = 'labConfiguration'


