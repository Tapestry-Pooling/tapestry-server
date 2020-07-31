from django.contrib import admin
from rest.models import Test


class TestAdmin(admin.ModelAdmin):
    list_display = ('id', 'nsamples', 'assigned_to', 'npositive', 'inconclusive', 'prevalence', 'status', 'remark')

admin.site.register(Test, TestAdmin)