from rest_framework import viewsets
from rest.models import Test
from rest.serializers import TestSerializer

class TestViewset(viewsets.ModelViewSet):
   queryset = Test.objects.all()
   serializer_class = TestSerializer
   filterset_fields = {
       'status__name': ('icontains', 'iexact', 'contains'),
    }
   search_fields = ['id',]