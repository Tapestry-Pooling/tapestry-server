from rest_framework_json_api import serializers
from rest.models import LabMember


class LabMemberSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = LabMember
        fields = ['url', 'name', 'designation', 'phone_number', 'email', 'lab_id']
