import os
from django import forms

from rest.models import LabConfiguration
from rest.util.gc_util import get_object_list


class LabConfigurationForm(forms.ModelForm):
    poolingmatrix_filename = forms.ChoiceField(
        choices=get_object_list(bucket_name=os.environ.get('KIRKMAN_MATRIX_BUCKET'))
    )
    class Meta:
        model = LabConfiguration
        fields = ('lab_id', 'machine_type', 'test_kit', 'nsamples', 'prevalence', 'max_poolsize', 'poolingmatrix_filename')