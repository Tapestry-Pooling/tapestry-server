from django.contrib import admin

from rest.models import LabConfiguration
from rest.forms import LabConfigurationForm


class LabConfigurationAdmin(admin.ModelAdmin):
    add_form = LabConfigurationForm
    form = LabConfigurationForm
    model = LabConfiguration
    list_display = ('id', 'lab_id', 'nsamples', 'prevalence', 'max_poolsize', 'poolingmatrix_filename')


admin.site.register(LabConfiguration, LabConfigurationAdmin)