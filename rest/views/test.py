from rest_framework import viewsets
from rest.models import Test
from rest.serializers import TestSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters



class TestViewSet(viewsets.ModelViewSet):
    queryset = Test.objects.all()
    serializer_class = TestSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['status',    ]
    search_fields = ['id', ]

    def get_queryset(self):
        user = self.request.user
        return Test.objects.filter(assigned_to__lab_id=user.lab_id)