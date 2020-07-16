from rest_framework_json_api import serializers
from rest.models import Test

class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = ['id', 'assigned_to', 'status', 'samples', 'suspected_samples', 'positive_samples', 'test_kit', 'machine_type', 'remark', 'file', 'pooling_matrix', 'mastermix_matrix', 'patient_id_map', 'results_1', 'results_2']

