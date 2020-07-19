from django.contrib import admin
from rest.models import MachineType


class MachineTypeAdmin(admin.ModelAdmin):
    pass

admin.site.register(MachineType, MachineTypeAdmin)