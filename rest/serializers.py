from rest_framework_json_api import serializers
from rest_framework_json_api.relations import ResourceRelatedField, HyperlinkedRelatedField
from .models import Lab, LabMember


class LabMemberSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = LabMember
        fields = ['url', 'name', 'designation', 'phone_number', 'email', 'lab_id']


class LabSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Lab
        fields = ['url', 'name', 'city', 'country']


