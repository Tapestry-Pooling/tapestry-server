from rest_framework import viewsets
from rest.models import Test
from rest.serializers import TestSerializer
from rest_framework_json_api import django_filters
from rest_framework_json_api import filters
from rest_framework.filters import SearchFilter


class TestViewSet(viewsets.ModelViewSet):
    queryset = Test.objects.all()
    serializer_class = TestSerializer
    filter_backends =(filters.QueryParameterValidationFilter, django_filters.DjangoFilterBackend, SearchFilter)
    filterset_fields = {'status': ('exact', 'in'),}
    search_fields = ['id', ]

    def get_queryset(self):
        user = self.request.user
        return Test.objects.filter(assigned_to__lab_id=user.lab_id)