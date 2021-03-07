from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _
from rest.models import Test, Status
from rest.util.admin_alert import test_review_alert_email_admin, file_error_alert_email_admin
from django.contrib import messages
from rest.util.user_alert import test_result_alert_user

class TestWebhookSerializer(serializers.Serializer):
    positive = serializers.JSONField()
    negative = serializers.JSONField()
    inconclusive = serializers.JSONField()
    report_filename = serializers.CharField(max_length=255)
    status = serializers.JSONField()
    message = serializers.CharField(max_length=255)


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
                self.test.npositive = len(attrs.get('positive'))
                self.test.nnegative = len(attrs.get('negative'))
                self.test.ninconclusive = len(attrs.get('inconclusive'))
                self.test.genes = attrs.get('genes')
                self.test.positive = attrs.get('positive')
                self.test.negative = attrs.get('negative')
                self.test.inconclusive = attrs.get('inconclusive')
                self.test.report_filename =attrs.get('report_filename')
                self.test.status = Status.objects.get(name='COMPLETED')

                # alert user
                positive_sample_list = [entry['sample'] for entry in self.test.positive]
                inconclusive_sample_list = [entry['sample'] for entry in self.test.inconclusive]
                test_result_alert_user(self.test.assigned_to, self.test.pk, positive_sample_list, inconclusive_sample_list)

                # messages.info(
                #     request,
                #     "Test {} status set to COMPLETED".format(id)
                # )
                if (len(self.test.positive[0][list(self.test.positive[0].keys())[0]])!=len(self.test.genes)):
                    self.test.err_msg = "Number of genes does not match"
                    self.test.status = Status.objects.get(pk=3)

            else:
                self.test.err_msg = attrs.get('message')
                self.test.status = Status.objects.get(pk=3)
        except Test.DoesNotExist:
            print('Test ID does not exist')
            # alert admin
            file_error_alert_email_admin(filename=report_filename, error_status=status)

        return attrs

    def save(self):
        self.test.save()

        # alert admin
        test_review_alert_email_admin(test_id=self.test.pk, positive=self.test.positive, inconclusive=self.test.inconclusive)
