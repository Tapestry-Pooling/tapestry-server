from rest.models import Country
from rest_framework_json_api import serializers

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ('name','calling_codes','alpha_2_code','alpha_3_code')