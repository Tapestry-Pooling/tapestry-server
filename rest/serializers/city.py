from rest.models import City
from rest_framework_json_api import serializers

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ('name','country')