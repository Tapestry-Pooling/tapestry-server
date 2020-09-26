from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _
from rest.models import Test
from rest.util.admin_alert import test_review_alert_email_admin


class TestWebhookSerializer(serializers.Serializer):
    positive = serializers.JSONField()
    negative = serializers.JSONField()
    inconclusive = serializers.JSONField()
    report_filename = serializers.CharField(max_length=255)
    results_filename = serializers.CharField(max_length=255)

    def __init__(self, *args, **kwargs):
        super(TestWebhookSerializer, self).__init__(*args, **kwargs)

    def validate(self, attrs):
        # check if report_filename exists
        report_filename = attrs.get('report_filename')
        try:
            self.test = Test.objects.get(testctresults_filename=results_filename)
        except Test.DoesNotExist:
            raise serializers.ValidationError(_('Test does not exist'))

        return attrs

    def save(self):
        self.test.npositive = len(self.validated_data['positive'])
        self.test.nnegative = len(self.validated_data['negative'])
        self.test.ninconclusive = len(self.validated_data['inconclusive'])
        self.test.positive = self.validated_data['positive']
        self.test.negative = self.validated_data['negative']
        self.test.inconclusive = self.validated_data['inconclusive']
        self.test.report_filename = self.validated_data['report_filename']
        self.test.save()
        
        # alert admin
        test_review_alert_email_admin(test_id=self.test.pk)
