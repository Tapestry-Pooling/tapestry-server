from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from rest.forms import CustomUserCreationForm, CustomUserChangeForm
from rest.models import User
from django.utils.html import format_html
from django.urls import reverse
from django.conf.urls import url
from django.http import HttpResponseRedirect

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ('email', 'is_staff', 'is_active', 'designation', 'lab_id','activate')
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_superuser', 'is_staff', 'is_active')}),
        ('Details', {'fields': ('first_name', 'last_name', 'phone_number', 'designation', 'lab_id')})
    )
    add_fieldsets = (
        (None, {'fields': ('email', 'password1', 'password2')}),
        ('Permissions', {'fields': ('is_superuser', 'is_staff', 'is_active')}),
        ('Details', {'fields': ('first_name', 'last_name', 'phone_number', 'designation', 'lab_id')})
    )
    search_fields = ('email',)
    ordering = ('email',)
    
    def activate(self, obj):
        return format_html(
            '<a class="button" href="{}">View Token</a>&nbsp;',
            reverse('admin:activate-user, args=[obj.pk]'),
        )
    activate.short_description = 'Activate User'
    activate.allow_tags = True

    def handle_activate_uer(self, request, id, *args, **kwargs):
        # app = Application.objects.get(id = application_id)
        # AccessToken.objects.get(application = app).delete()
        print("Custom code here...")
        return HttpResponseRedirect("../../")

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            url(
                r'^(?P<id>.+)/activate-user/$',
                self.admin_site.admin_view(self.handle_activate_uer),
                name='activate-user'),
        ]
        return custom_urls + urls


admin.site.register(User, CustomUserAdmin)