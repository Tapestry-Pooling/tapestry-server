from rest_framework_json_api import serializers
from rest.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'designation', 'phone_number', 'lab_id']