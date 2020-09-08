from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from rest.forms import CustomUserCreationForm, CustomUserChangeForm
from rest.models import User, LabConfiguration
from django.utils.html import format_html
from django.urls import reverse
from django.conf.urls import url
from django.http import HttpResponseRedirect
from allauth.account.utils import send_email_confirmation
from django.contrib.auth.forms import PasswordResetForm
from pooling import settings
from allauth.account.models import EmailAddress
from django.contrib import messages


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ('email', 'is_staff', 'is_active', 'designation',
                    'lab_id', 'is_lab_config_added', 'activate')
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_superuser', 'is_staff', 'is_active')}),
        ('Details', {'fields': ('first_name', 'last_name',
                                'phone_number', 'designation', 'lab_id')})
    )
    add_fieldsets = (
        (None, {'fields': ('email', 'password1', 'password2')}),
        ('Permissions', {'fields': ('is_superuser', 'is_staff', 'is_active')}),
        ('Details', {'fields': ('first_name', 'last_name',
                                'phone_number', 'designation', 'lab_id')})
    )
    search_fields = ('email',)
    ordering = ('email',)

    def activate(self, obj):
        if obj.is_staff:
            return None

        email_address = EmailAddress.objects.get(email=obj.email)
        if email_address.verified:
            return None

        return format_html(
            '<a class="button" href="{}">Activate User</a>&nbsp;',
            reverse('admin:activate-user', args=[obj.pk]),
        )

    activate.short_description = 'Activate User'
    activate.allow_tags = True

    def handle_activate_user(self, request, id, *args, **kwargs):

        user = User.objects.get(pk=id)

        # check if lab configuration is added
        if not LabConfiguration.objects.filter(lab_id=user.lab_id).exists():
            messages.error(
                request,
                "Lab configuration is not added!"
            )
            return HttpResponseRedirect("../../")

        user.is_active = True
        # user.password = get_random_string(length=32)
        user.save(force_update=True)

        # send_email_confirmation(request,user, False)
        reset_form = PasswordResetForm(data={'email': user.email})
        reset_form.is_valid()

        opts = {
            'use_https': request.is_secure(),
            'from_email': settings.DEFAULT_FROM_EMAIL,
            'request': request,
            'subject_template_name': 'registration/set_password_subject.txt',
            'email_template_name': 'registration/set_password.html',
            'html_email_template_name': 'registration/set_password.html'
        }
        reset_form.save(**opts)

        messages.info(
            request,
            "{} has been activated!".format(user.email)
        )

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

    def is_lab_config_added(self, obj):
        if obj.is_staff:
            return True
        if LabConfiguration.objects.filter(lab_id=obj.lab_id).exists():
            return True
        return False

    is_lab_config_added.boolean = True
    is_lab_config_added.short_description = "Lab Configuration Added"


admin.site.register(User, CustomUserAdmin)
