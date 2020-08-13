from rest_framework_json_api import serializers
from rest.models import Lab


class LabSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lab
        fields = ['id', 'name', 'city', 'country']