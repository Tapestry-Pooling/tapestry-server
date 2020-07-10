from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import api_view

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser

from rest.models.machine_type import MachineType
from rest.serializers.machine_type import MachineTypeSerializer

class MachineTypeViewset(viewsets.ModelViewSet):
    queryset = MachineType.objects.all()
    serializer_class = MachineTypeSerializer

