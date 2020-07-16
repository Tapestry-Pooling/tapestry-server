from rest_framework_json_api import serializers
from rest.models import Matrix

class MatrixSerializer(serializers.ModelSerializer):
    class Meta:
        model = Matrix
        fields = ['id', 'kirkman_matrix']