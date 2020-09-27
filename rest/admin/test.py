from django.utils.html import format_html
from django.contrib import admin
from rest.models import Test, Status
from rest.forms import TestForm
from rest.util.gc_util import get_report_download_url
from django.urls import reverse
from django.conf.urls import url
from django.http import HttpResponseRedirect
from django.contrib import messages


class TestAdmin(admin.ModelAdmin):
    add_form = TestForm
    form = TestForm
    model = Test
    list_display = ('id', 'status', 'assigned_to','nsamples', 'npositive', 'ninconclusive', 'prevalence', 'report_filename', 'set_completed', 'download_report', )

    def download_report(self, obj):
        if obj.report_filename:
            return format_html(
                '<a class="Button" href="{}" target="_blank">Download</a>&nbsp;',
                reverse('admin:download-report', args=[obj.pk]),
            )
        return None

    def handle_download_report(self, request, id, *args, **kwargs):
        test = Test.objects.get(pk=id)
        url = get_report_download_url(test.report_filename)
        return HttpResponseRedirect(url)

    download_report.allow_tags = True

    def set_completed(self, obj):
        if obj.report_filename and obj.status.name != 'COMPLETED':
            return format_html(
                '<a class="button" href="{}">Approve</a>&nbsp;',
                reverse('admin:set-completed', args=[obj.pk]),
            )
        return None

    def handle_set_completed(self, request, id, *args, **kwargs):
        test = Test.objects.get(pk=id)
        test.status = Status.objects.get(name='COMPLETED')
        test.save()
        messages.info(
            request,
            "Test {} status set to COMPLETED".format(id)
        )
        return HttpResponseRedirect("../../")

    set_completed.short_description = "SET COMPLETED"
    set_completed.allow_tags = True

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            url(
                r'^(?P<id>.+)/set-completed/$',
                self.admin_site.admin_view(self.handle_set_completed),
                name='set-completed'
            ),
            url(
                r'^(?P<id>.+)/download-report/$',
                self.admin_site.admin_view(self.handle_download_report),
                name='download-report'
            )
        ]
        return custom_urls + urls

admin.site.register(Test, TestAdmin)