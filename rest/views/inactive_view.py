from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from django.utils.translation import ugettext_lazy as _


@api_view(['GET'])
def inactive_view(request):
    return Response({'detail': _('inactive user')}, status=status.HTTP_200_OK)