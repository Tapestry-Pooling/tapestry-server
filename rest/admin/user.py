from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from rest.forms import CustomUserCreationForm, CustomUserChangeForm
from rest.models import User
from django.utils.html import format_html
from django.urls import reverse
from django.conf.urls import url
from django.http import HttpResponseRedirect
from allauth.account.utils import send_email_confirmation
from django.contrib.auth.forms import PasswordResetForm
from pooling import settings

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
        if obj.is_staff:
            return None
        return format_html(
            '<a class="button" href="{}">Activate User</a>&nbsp;',
            reverse('admin:activate-user', args=[obj.pk]),
        )
    activate.short_description = 'Activate User'
    activate.allow_tags = True

    def handle_activate_user(self, request, id, *args, **kwargs):

        user = User.objects.get(pk= id)
        user.is_active = True
        # user.password = get_random_string(length=32)
        user.save(force_update=True)

        # send_email_confirmation(request,user, False)
        reset_form = PasswordResetForm(data={'email':user.email})
        reset_form.is_valid()

        opts = {
            'use_https': request.is_secure(),
            'from_email': settings.DEFAULT_FROM_EMAIL,
            'request': request,
        }
        reset_form.save(**opts)
        
        return HttpResponseRedirect("../../")

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            url(
                r'^(?P<id>.+)/activate-user/$',
                self.admin_site.admin_view(self.handle_activate_user),
                name='activate-user'),
        ]
        return custom_urls + urls


admin.site.register(User, CustomUserAdmin)