from rest_framework_json_api import serializers
from rest.models import Test
from rest.util.gc_util import get_pooling_matrix_download_url


class TestSerializer(serializers.ModelSerializer):
    pooling_matrix_download_url = serializers.ReadOnlyField()
    class Meta:
        model = Test
        exclude = ['poolingscheme_filename', 'testctresults_filename', 'report_filename']
        read_only_fields = ['status', 'npositive', 'ninconclusive', 'nnegative', 'positive', 'negative', 'inconclusive', 'poolingmatrix_filename']

    def get_pooling_matix_url(self, test):
        payload = {
            "nsamples": test.nsamples,
            "prevalence": test.prevalence,
            "genes": ", ".join(test.test_kit.gene_type),
            "testid": test.pk,
            "lab_name": test.assigned_to.lab_id.__str__(),
            "poolingmatrix_filename": test.poolingmatrix_filename
        }
        return get_pooling_matrix_download_url(payload=payload)

    def create(self, validated_data):
        test = Test.objects.create(**validated_data)
        payload = {
            "nsamples": test.nsamples,
            "prevalence": test.prevalence,
            "genes": ", ".join(test.test_kit.gene_type),
            "testid": test.pk,
            "lab_name": test.assigned_to.lab_id.__str__(),
            "poolingmatrix_filename": test.poolingmatrix_filename
        }
        try:
            test.poolingscheme_filename, test.pooling_matrix_download_url = get_pooling_matrix_download_url(test)
            test.save()
        except Exception as e:
            print(e)
        return test
