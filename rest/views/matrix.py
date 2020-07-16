from rest_framework import viewsets
from rest.models import Matrix
from rest.serializers import MatrixSerializer


class MatrixViewset(viewsets.ModelViewSet):
    queryset = Matrix.objects.all()
    serializer_class = MatrixSerializer