from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _
from rest.models import Test


class UploadUrlSerializer(serializers.Serializer):
    test_id = serializers.IntegerField()
    file_name = serializers.CharField(max_length=128)

    def __init__(self, *args, **kwargs):
        super(UploadUrlSerializer, self).__init__(*args, **kwargs)

        self.request = self.context.get('request')
        self.user = getattr(self.request, 'user', None)

    def validate(self, attrs):
        test_id = attrs.get('test_id')

        # check if test_id is valid
        try:
            self.test = Test.objects.get(pk=test_id)
        except Test.DoesNotExist:
            raise serializers.ValidationError(_('Invalid test_id'))

        # check if user and test belong to the same lab
        if self.test.assigned_to.lab_id != self.user.lab_id:
            raise serializers.ValidationError(_('Invalid test_id'))

        return attrs

    def save(self):
        pass