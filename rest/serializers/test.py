from rest_framework_json_api import serializers
from rest.models import Test

class TestSerializer(serializers.ModelSerializer):
    pooling_matrix_url = serializers.ReadOnlyField()
    class Meta:
        model = Test
        fields = '__all__'