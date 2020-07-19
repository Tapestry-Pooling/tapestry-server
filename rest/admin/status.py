from django.contrib import admin
from rest.models import Status


class StatusAdmin(admin.ModelAdmin):
    pass

admin.site.register(Status, StatusAdmin)