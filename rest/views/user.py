from rest_framework import viewsets
from rest.models import User
from rest.serializers import UserSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        users = User.objects.filter(lab_id=self.request.user.lab_id)
        return users