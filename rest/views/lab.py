from rest_framework import viewsets
from rest.models import Lab
from rest.serializers import LabSerializer
from rest.permissions import IsLabOwnerOrAdmin
from rest_framework.permissions import IsAdminUser


class LabViewSet(viewsets.ModelViewSet):
    queryset = Lab.objects.all()
    serializer_class = LabSerializer

    def get_permissions(self):
        if self.action in ['list', 'create']:
            self.permission_classes = [IsAdminUser, ]
        else:
            self.permission_classes = [IsLabOwnerOrAdmin, ]
        return super(self.__class__, self).get_permissions()