from django.contrib import admin
from rest.models import Lab


class LabAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'city', 'country')


admin.site.register(Lab, LabAdmin)
