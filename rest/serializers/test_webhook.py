from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _
from rest.models import Test, Status
from rest.util.admin_alert import test_review_alert_email_admin, file_error_alert_email_admin


class TestWebhookSerializer(serializers.Serializer):
    positive = serializers.JSONField()
    negative = serializers.JSONField()
    inconclusive = serializers.JSONField()
    report_filename = serializers.CharField(max_length=255)
    status = serializers.JSONField()

    def __init__(self, *args, **kwargs):
        super(TestWebhookSerializer, self).__init__(*args, **kwargs)

    def validate(self, attrs):
        # check if report_filename exists
        report_filename = attrs.get('report_filename')
        status = attrs.get('status')['code']
        try:
            testID = report_filename.split("_TEST_")[1].split('_')[0]
            self.test = Test.objects.get(pk=testID)

            if status == 200:
                self.test.npositive = len(self.validated_data['positive'])
                self.test.nnegative = len(self.validated_data['negative'])
                self.test.ninconclusive = len(self.validated_data['inconclusive'])
                self.test.positive = self.validated_data['positive']
                self.test.negative = self.validated_data['negative']
                self.test.inconclusive = self.validated_data['inconclusive']
                self.test.report_filename = self.validated_data['report_filename']
                self.test.status = Status.objects.get(pk=2)
            else:
                self.test.err_msg = attrs.get('status')['reason']
                self.test.status = Status.objects.get(pk=3)
        except Test.DoesNotExist:
            print('Test ID does not exist')
            # alert admin
            file_error_alert_email_admin(filename=report_filename, error_status=status)

        return attrs

    def save(self):
        self.test.save()

        # alert admin
        test_review_alert_email_admin(test_id=self.test.pk)
