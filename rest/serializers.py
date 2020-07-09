from rest_framework_json_api import serializers
from .models import MachineType, TestKit, LabConfiguration

class MachineTypeSerializer(serializers.ModelSerializer):
	class Meta:
		model = MachineType
		fields = ['id', 'name', 'no_of_wells', 'plate_x', 'plate_y']

class TestKitSerializer(serializers.ModelSerializer):
	class Meta:
		model = TestKit
		fields = ['id', 'name', 'description']

class LabConfigurationSerializer(serializers.ModelSerializer):
	class Meta:
		model = LabConfiguration
		fields = ['id', 'lab_id', 'machine_type', 'test_kit']