from rest_framework import viewsets
from rest.models import Test
from rest_framework_json_api import django_filters
from rest_framework.filters import SearchFilter
from rest.serializers import TestSerializer
from rest.permissions import IsLabTestOwnerOrAdmin


class LabTestViewSet(viewsets.ModelViewSet):
    serializer_class = TestSerializer
    permission_classes = (IsLabTestOwnerOrAdmin, )
    filter_backends = (django_filters.DjangoFilterBackend, SearchFilter)
    filterset_fields = {'status': ('exact', 'in'), }
    search_fields = ['=id', ]

    def get_queryset(self):
        return Test.objects.filter(assigned_to__lab_id=self.kwargs['lab_pk']).order_by('id').desc()
