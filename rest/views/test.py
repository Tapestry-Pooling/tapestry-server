from rest_framework import viewsets
from rest.models import Test
from rest.serializers import TestSerializer
from rest_framework.response import Response
from rest.util.gcf_call import pooling_matrix_gcf
import json


class TestViewSet(viewsets.ModelViewSet):
    queryset = Test.objects.all()
    serializer_class = TestSerializer
    filterset_fields = {
        'status__name': ('icontains', 'iexact', 'contains'),
    }
    search_fields = ['id', ]

    def create(self, request, *args, **kwargs):
        serializer = TestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # generate signed url
        test = Test.objects.get(pk=serializer.data['id'])
        payload = {
            "nsamples": test.samples,
            "prevalence": test.prevalence,
            "genes": ", ".join(test.test_kit.gene_type),
            "testid": test.id,
            "lab_name": test.assigned_to.lab_id.__str__()
        }
        pooling_matrix_status_code, pooling_matrix_url = pooling_matrix_gcf(payload=json.dumps(payload))
        return Response(
            {
                "pooling_matrix_status_code": pooling_matrix_status_code,
                "pooling_matrix_url": pooling_matrix_url,
                "test": serializer.data
            }
        )
