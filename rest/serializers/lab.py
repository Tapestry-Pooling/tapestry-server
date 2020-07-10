from rest_framework_json_api import serializers
from rest.models import Lab


class LabSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Lab
        fields = ['url', 'name', 'city', 'country']