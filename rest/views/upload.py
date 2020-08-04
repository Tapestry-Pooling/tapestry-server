from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from rest.util.gc_util import get_ct_value_upload_url
from rest.util.util import check_and_fix_upload_file_name
from rest.serializers import UploadUrlSerializer


class UploadUrlView(GenericAPIView):
    serializer_class = UploadUrlSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        upload_url = get_ct_value_upload_url(
            "{}".format(check_and_fix_upload_file_name(
                    serializer.validated_data['test_id'],
                    serializer.validated_data['file_name']
                )
            )
        )
        return Response({"upload_url": upload_url}, status.HTTP_200_OK)