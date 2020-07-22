from rest_framework import viewsets
from rest.models import Status
from rest.serializers import StatusSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class StatusViewset(viewsets.ModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer

    