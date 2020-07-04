from rest_framework import viewsets, permissions
from languages.models import Programmer
from languages.serializers import ProgrammerSerializer

class ProgrammerView(viewsets.ModelViewSet):
    queryset = Programmer.objects.all()
    serializer_class = ProgrammerSerializer

