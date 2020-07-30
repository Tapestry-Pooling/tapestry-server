from django.db import models

class MachineType(models.Model) :
	name = models.CharField(max_length=60, blank=False, default='PCR machine')
	machine_maker = models.CharField(max_length=50, blank=False, default='')
	no_of_wells = models.SmallIntegerField()
	dim_x = models.SmallIntegerField(default=12)
	dim_y = models.SmallIntegerField(default=8)
	capacity = models.FloatField(null=True)
	resource_name = 'machineType'


