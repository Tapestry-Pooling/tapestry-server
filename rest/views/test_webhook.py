from rest_framework.generics import GenericAPIView

from rest.serializers import TestWebhookSerializer


class TestWebhookView(GenericAPIView):
    serializer_class = TestWebhookSerializer
    http_method_names = ('POST', )