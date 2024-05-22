from django.db.models import Count, Q
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import (OpenApiExample, OpenApiParameter,
                                   extend_schema)
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .enums import CompressionStatus
from .models import MediaFile
from .serializers import ListMediaSerializer, UploadMediaSerializer


class MediaFileViewSet(ModelViewSet):
    queryset = MediaFile.objects.all()
    serializer_class = ListMediaSerializer
    permission_classes = [AllowAny]
    http_method_names = ["get", "post"]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ["user", "file_name"]
    filterset_fields = [
        "compression_status",
    ]

    def get_queryset(self):
        request: Request = self.request
        user: str = request.query_params.get("user")
        if not user:
            return super().get_queryset().none()
        return super().get_queryset().filter(user=user.lower())

    @extend_schema(
        parameters=[
            OpenApiParameter("user", str, OpenApiParameter.QUERY, required=True)
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        parameters=[
            OpenApiParameter("user", str, OpenApiParameter.QUERY, required=True)
        ]
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(request=UploadMediaSerializer, responses={200, ListMediaSerializer})
    def create(self, request: Request, *args, **kwargs):
        serializer = UploadMediaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response(ListMediaSerializer(instance).data, status=201)

    @extend_schema(
        parameters=[
            OpenApiParameter("user", str, OpenApiParameter.QUERY, required=True)
        ],
        examples=[
            OpenApiExample(
                name="Dashboard Stat example",
                value={
                    "success": True,
                    "data": {
                        "uploaded": 0,
                        "compressed": 0,
                        "failed": 0,
                        "in_progress": 0,
                    },
                },
            )
        ],
    )
    @action(
        methods=["GET"],
        detail=False,
        url_path="stat",
    )
    def stat(self, request: Request):
        user: str = self.request.query_params.get("user")
        if not user:
            return Response({"detail": "Empty user query param"}, status=400)
        qs = MediaFile.objects.filter(user=user.lower())
        uploaded = Count("id")
        compressed = Count(
            "id", filter=Q(compression_status=CompressionStatus.COMPLETED)
        )
        failed = Count("id", filter=Q(compression_status=CompressionStatus.CANCELLED))
        in_progress = Count(
            "id",
            filter=Q(
                compression_status__in=[
                    CompressionStatus.DEFAULT,
                    CompressionStatus.CONVERTING,
                ]
            ),
        )

        data = qs.aggregate(
            uploaded=uploaded,
            compressed=compressed,
            failed=failed,
            in_progress=in_progress,
        )
        return Response(data={"success": True, "data": data}, status=200)
