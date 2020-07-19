from django.contrib import admin
from rest.models import TestKit


class TestKitAdmin(admin.ModelAdmin):
    pass

admin.site.register(TestKit, TestKitAdmin)