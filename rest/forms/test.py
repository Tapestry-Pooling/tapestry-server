import os
from django import forms

from rest.models import Test
from rest.util.gc_util import get_object_list


class TestForm(forms.ModelForm):
    poolingmatrix_filename = forms.ChoiceField(
        choices=get_object_list(bucket_name=os.environ.get('KIRKMAN_MATRIX_BUCKET'))
    )
    class Meta:
        model = Test
        fields = ('assigned_to', 'machine_type', 'test_kit', 'nsamples', 'prevalence', 'max_poolsize', 'poolingmatrix_filename', 'remark', 'npositive', 'ninconclusive', 'nnegative', 'positive', 'negative', 'inconclusive')