from rest_framework import viewsets
from rest.models import LabMember
from rest.serializers import LabMemberSerializer


class LabMemberViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = LabMember.objects.all()
    serializer_class = LabMemberSerializer

