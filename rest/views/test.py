from rest_framework import viewsets
from rest.models import Test
from rest.serializers import TestSerializer
from rest_framework_json_api import django_filters
from rest_framework.filters import SearchFilter
from rest.permissions import IsTestOwnerOrAdmin
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import action
from rest.util.gc_util import get_pooling_matrix_download_url, get_report_download_url, get_result_download_url
from rest_framework.response import Response
from rest_framework import status


class TestViewSet(viewsets.ModelViewSet):
    queryset = Test.objects.all()
    serializer_class = TestSerializer
    filter_backends = (django_filters.DjangoFilterBackend, SearchFilter)
    filterset_fields = {'status': ('exact', 'in'), }
    search_fields = ['=id', ]

    def get_permissions(self):
        if self.action == 'list':
            self.permission_classes = [IsAdminUser, ]
        else:
            self.permission_classes = [IsTestOwnerOrAdmin, ]
        return super(self.__class__, self).get_permissions()

    @action(detail=True, permission_classes=(IsTestOwnerOrAdmin,))
    def pooling_matrix(self, request, pk=None):
        try:
            test = Test.objects.get(pk=pk)
        except Test.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        return Response(
            {
                "pooling_matrix_download_url": get_pooling_matrix_download_url(
                    object_name=test.poolingscheme_filename
                )[1]
            },
            status=status.HTTP_200_OK
        )

    @action(detail=True, permission_classes=(IsTestOwnerOrAdmin,))
    def report(self, request, pk=None):
        try:
            test = Test.objects.get(pk=pk)
        except Test.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        return Response(
            {
                "report_download_url": get_report_download_url(
                    object_name=test.report_filename
                )
            },
            status=status.HTTP_200_OK
        )

    @action(detail=True, permission_classes=(IsTestOwnerOrAdmin,))
    def result(self, request, pk=None):
        try:
            test = Test.objects.get(pk=pk)
        except Test.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        return Response(
            {
                "result_download_url": get_result_download_url(
                    object_name=test.testctresults_filename
                )
            },
            status=status.HTTP_200_OK
        )