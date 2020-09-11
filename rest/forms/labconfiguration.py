import os
from django import forms

from rest.models import LabConfiguration
from rest.util.gc_util import get_object_list


class LabConfigurationForm(forms.ModelForm):
    poolingmatrix_filename = forms.ChoiceField(
        choices=get_object_list(
            'kirkman_matrices_prod' if os.environ.get('DJANGO_ENV') == 'prod' else 'kirkman_matrices'
        )
    )
    class Meta:
        model = LabConfiguration
        fields = ('lab_id', 'machine_type', 'test_kit', 'nsamples', 'prevalence', 'max_poolsize', 'poolingmatrix_filename')