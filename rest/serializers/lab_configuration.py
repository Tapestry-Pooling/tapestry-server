from rest_framework_json_api import serializers
from rest.models.lab_configuration import LabConfiguration

class LabConfigurationSerializer(serializers.ModelSerializer):
	class Meta:
		model = LabConfiguration
		fields = ['id', 'lab_id', 'machine_type', 'test_kit']