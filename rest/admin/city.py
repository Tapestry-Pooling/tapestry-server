from django.contrib import admin
from rest.models import City


class CityAdmin(admin.ModelAdmin):
    pass

admin.site.register(City, CityAdmin)
