from rest_framework import viewsets
from rest.models import Lab
from rest.serializers import LabSerializer


class LabViewSet(viewsets.ModelViewSet):
    queryset = Lab.objects.all()
    serializer_class = LabSerializer