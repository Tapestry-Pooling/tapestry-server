from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _
from rest.models import Test
from rest.models import Status


import re

from rest.util.util import check_and_fix_upload_file_name


class UploadUrlSerializer(serializers.Serializer):
    file_name = serializers.CharField(max_length=128)

    def __init__(self, *args, **kwargs):
        super(UploadUrlSerializer, self).__init__(*args, **kwargs)

        self.request = self.context.get('request')
        self.user = getattr(self.request, 'user', None)

    def validate(self, attrs):
        self.test_id = self.context.get('view').kwargs['id']
        file_name = attrs.get('file_name')

        # check if test_id is valid
        try:
            self.test = Test.objects.get(pk=self.test_id)
        except Test.DoesNotExist:
            raise serializers.ValidationError(_('Invalid test id'))

        # check if user and test belong to the same lab
        if not self.user.is_staff and self.test.assigned_to.lab_id != self.user.lab_id:
            raise serializers.ValidationError(_('Invalid test id'))

        # validate file name
        file_name_pattern = "^.*.xlsx$"
        if not re.search(file_name_pattern, file_name):
            raise serializers.ValidationError(_('only xlsx file accepted'))

        return attrs

    def save(self):
        self.test.status = Status.objects.get(pk=2)
        self.test.testctresults_filename = check_and_fix_upload_file_name(
            self.test_id,
            self.validated_data['file_name']
        )
        self.test.save()