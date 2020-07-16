from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from rest.forms import CustomUserCreationForm, CustomUserChangeForm
from rest.models import User


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ('email', 'is_staff', 'is_active', 'designation', 'lab_id')
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


admin.site.register(User, CustomUserAdmin)