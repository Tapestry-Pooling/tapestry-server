from django.db import models

class MachineType(models.Model) :
	name = models.CharField(max_length=60, blank=False, default='PCR machine')
	no_of_wells = models.SmallIntegerField()
	plate_x = models.SmallIntegerField(default=12)
	plate_y = models.SmallIntegerField(default=8)
	resource_name = 'machineType'


