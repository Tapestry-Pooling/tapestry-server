from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import api_view

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser

from django_filters import rest_framework as filters

from rest.models.lab_configuration import LabConfiguration
from rest.serializers.lab_configuration import LabConfigurationSerializer

class LabConfigurationViewset(viewsets.ModelViewSet):
    queryset = LabConfiguration.objects.all()
    serializer_class = LabConfigurationSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('lab_id',)
