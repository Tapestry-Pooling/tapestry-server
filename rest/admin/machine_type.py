from django.contrib import admin
from rest.models import MachineType


class MachineTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'machine_maker')

admin.site.register(MachineType, MachineTypeAdmin)