from rest_framework import viewsets
from rest.models import User
from rest.serializers import UserSerializer


class LabViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer