from django.core.files.uploadedfile import UploadedFile
from rest_framework import serializers

from .models import MediaFile


class ListMediaSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = MediaFile
        fields = [
            "id",
            "user",
            "original_size",
            "new_size",
            "mimetype",
            "preview",
            "file_name",
            "compression_status",
            "duration",
            "thumbnail",
            "url",
            "created_at",
        ]

    def get_url(self, obj: MediaFile) -> str:
        return obj.url()


class UploadMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaFile
        fields = ["upload", "user"]

    def create(self, validated_data: dict):
        file_uploaded: UploadedFile = validated_data.get("upload")
        data = {
            "original_size": MediaFile.convert_bytes(file_uploaded.size, "mega"),
            "file_name": file_uploaded.name,
            "mimetype": file_uploaded.content_type,
            "user": validated_data.get("user").lower(),
            "upload": file_uploaded,
        }
        new_instance = MediaFile.objects.create(**data)
        return new_instance
