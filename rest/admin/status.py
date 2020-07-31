from django.contrib import admin
from rest.models import Status


class StatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

admin.site.register(Status, StatusAdmin)