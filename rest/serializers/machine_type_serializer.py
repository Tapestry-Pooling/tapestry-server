from rest_framework_json_api import serializers
from rest.models.machine_type_model import MachineType

class MachineTypeSerializer(serializers.ModelSerializer):
	class Meta:
		model = MachineType
		fields = ['id', 'name', 'no_of_wells', 'plate_x', 'plate_y']
