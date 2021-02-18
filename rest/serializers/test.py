from rest_framework_json_api import serializers
from rest.models import Test


class TestSerializer(serializers.ModelSerializer):
    pooling_matrix_download_url = serializers.ReadOnlyField()
    report_download_url = serializers.ReadOnlyField()
    result_download_url = serializers.ReadOnlyField() 
    class Meta:
        model = Test
        exclude = ['poolingscheme_filename', 'testctresults_filename', 'report_filename']
        read_only_fields = ['err_msg', 'status', 'npositive', 'ninconclusive', 'nnegative', 'positive', 'negative', 'inconclusive', 'poolingmatrix_filename']