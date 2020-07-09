from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import api_view

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser

from rest.models.test_kit import TestKit
from rest.serializers.test_kit import TestKitSerializer

class TestKitViewset(viewsets.ModelViewSet):
    queryset = TestKit.objects.all()
    serializer_class = TestKitSerializer