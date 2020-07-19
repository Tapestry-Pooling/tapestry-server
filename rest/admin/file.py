from django.contrib import admin
from rest.models import File


class FileAdmin(admin.ModelAdmin):
    pass

admin.site.register(File, FileAdmin)
