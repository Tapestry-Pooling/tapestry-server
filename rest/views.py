from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import api_view

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser

from .models import MachineType, TestKit, LabConfiguration
from .serializers import MachineTypeSerializer, TestKitSerializer, LabConfigurationSerializer

# Create your views here.
class MachineTypeViewset(viewsets.ModelViewSet):
    queryset = MachineType.objects.all()
    serializer_class = MachineTypeSerializer

class TestKitViewset(viewsets.ModelViewSet):
    queryset = TestKit.objects.all()
    serializer_class = TestKitSerializer

class LabConfigurationViewset(viewsets.ModelViewSet):
    queryset = LabConfiguration.objects.all()
    serializer_class = LabConfigurationSerializer