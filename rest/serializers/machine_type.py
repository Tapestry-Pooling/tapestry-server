from rest_framework_json_api import serializers
from rest.models.machine_type import MachineType

class MachineTypeSerializer(serializers.ModelSerializer):
	class Meta:
		model = MachineType
		fields = ['id', 'name', 'no_of_wells', 'dim_x', 'dim_y']
