from rest_framework import viewsets, permissions
from languages.models import Paradigm
from languages.serializers import ParadigmSerializer

class ParadigmView(viewsets.ModelViewSet):
    queryset = Paradigm.objects.all()
    serializer_class = ParadigmSerializer