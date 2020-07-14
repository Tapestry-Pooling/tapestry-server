from django.contrib import admin
from rest.models import Lab, LabMember


class LabMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'designation', 'lab')

    def lab(self, obj):
        return obj.lab_id.name
    lab.admin_order_field = 'lab_id__name'


admin.site.register(LabMember, LabMemberAdmin)