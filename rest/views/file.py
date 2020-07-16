from rest_framework import viewsets
from rest.models import File
from rest.serializers import FileSerializer


class FileViewset(viewsets.ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer