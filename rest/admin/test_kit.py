from django.contrib import admin
from rest.models import TestKit


class TestKitAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'kit_maker')

admin.site.register(TestKit, TestKitAdmin)