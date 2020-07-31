from django.contrib import admin
from rest.models import Test


class TestAdmin(admin.ModelAdmin):
    list_display = ('id', 'samples', 'assigned_to', 'status')

admin.site.register(Test, TestAdmin)