from rest_framework import viewsets, permissions
from languages.models import Language
from languages.serializers import LanguageSerializer

class LanguageView(viewsets.ModelViewSet):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer