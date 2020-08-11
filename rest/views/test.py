from rest_framework import viewsets
from rest.models import Test
from rest.serializers import TestSerializer
from rest_framework_json_api import django_filters
from rest_framework.filters import SearchFilter
from rest.permissions import IsTestOwnerOrAdmin
from rest_framework.permissions import IsAdminUser


class TestViewSet(viewsets.ModelViewSet):
    queryset = Test.objects.all()
    serializer_class = TestSerializer
    filter_backends = (django_filters.DjangoFilterBackend, SearchFilter)
    filterset_fields = {'status': ('exact', 'in'), }
    search_fields = ['=id', ]

    def get_permissions(self):
        if self.action == 'list':
            self.permission_classes = [IsAdminUser, ]
        else:
            self.permission_classes = [IsTestOwnerOrAdmin, ]
        return super(self.__class__, self).get_permissions()
