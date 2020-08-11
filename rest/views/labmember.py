from rest_framework import viewsets
from rest.models import User
from rest.serializers import UserSerializer
from rest.permissions import IsLabMemberOwnerOrAdmin


class LabMemberViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = (IsLabMemberOwnerOrAdmin, )

    def get_queryset(self):
        return User.objects.filter(lab_id=self.kwargs['lab_pk'])