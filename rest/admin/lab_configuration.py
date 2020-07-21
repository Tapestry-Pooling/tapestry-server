from django.contrib import admin
from rest.models import LabConfiguration


class LabConfigurationAdmin(admin.ModelAdmin):
    pass

admin.site.register(LabConfiguration, LabConfigurationAdmin)