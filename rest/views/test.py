from rest_framework import viewsets
from rest.models import Test
from rest.serializers import TestSerializer
from rest_framework_json_api import django_filters
from rest_framework import filters


class TestViewSet(viewsets.ModelViewSet):
    queryset = Test.objects.all()
    serializer_class = TestSerializer
    filter_backends = [django_filters.DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['status', ]
    search_fields = ['id', ]

    def get_queryset(self):
        user = self.request.user
        return Test.objects.filter(assigned_to__lab_id=user.lab_id)