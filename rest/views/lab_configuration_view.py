from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import api_view

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser

from rest.models.lab_configuration_model import LabConfiguration
from rest.serializers.lab_configuration_serializer import LabConfigurationSerializer

class LabConfigurationViewset(viewsets.ModelViewSet):
    queryset = LabConfiguration.objects.all()
    serializer_class = LabConfigurationSerializer