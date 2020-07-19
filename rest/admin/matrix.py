from django.contrib import admin
from rest.models import Matrix


class MatrixAdmin(admin.ModelAdmin):
    pass

admin.site.register(Matrix, MatrixAdmin)