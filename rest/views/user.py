from rest_framework import viewsets
from rest.models import User
from rest.serializers import UserSerializer
from rest.permissions import IsUserOwnerOrAdmin
from rest_framework.permissions import IsAdminUser


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == 'list':
            self.permission_classes = [IsAdminUser, ]
        else:
            self.permission_classes = [IsUserOwnerOrAdmin, ]
        return super(self.__class__, self).get_permissions()