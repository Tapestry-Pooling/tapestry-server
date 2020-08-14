from rest.models import Country
from rest_framework_json_api.views import ModelViewSet
from rest.serializers import CountrySerializer
from rest_framework.permissions import AllowAny

class CountryViewSet(ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = (AllowAny,)
    pagination_class = None