from rest_framework_json_api import serializers
from rest.models.test_kit import TestKit

class TestKitSerializer(serializers.ModelSerializer):
	class Meta:
		model = TestKit
		fields = ['id', 'name', 'description']
