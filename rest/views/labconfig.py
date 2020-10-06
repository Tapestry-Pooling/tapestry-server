from rest_framework import viewsets
from rest.models import LabConfiguration
from rest_framework_json_api import django_filters
from rest_framework.filters import SearchFilter
from rest.serializers import LabConfigurationSerializer


class LabConfigViewSet(viewsets.ModelViewSet):
    serializer_class = LabConfigurationSerializer
    pagination_class = None

    def get_queryset(self):
        return LabConfiguration.objects.filter(lab_id=self.kwargs['lab_pk'])