from django.contrib import admin
from rest.models import Test


class TestAdmin(admin.ModelAdmin):
    pass

admin.site.register(Test, TestAdmin)