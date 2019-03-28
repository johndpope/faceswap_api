from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework import status
from rest_framework.response import Response

from .models import FaceswapImage
from .serializers import (FaceswapImageSerializer,
                          FaceswapImageStatusSerializer)


class FaceswapImageView(CreateAPIView):
    serializer_class = FaceswapImageSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.additional_data,
            status=status.HTTP_201_CREATED,
            headers=headers,
        )


class FaceswapImageStatusView(RetrieveAPIView):
    serializer_class = FaceswapImageStatusSerializer
    queryset = FaceswapImage.objects.all()
    lookup_field = 'name'
