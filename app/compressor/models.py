from typing import Literal

from common.models import AuditableModel
from django.db import models

from .enums import CompressionStatus
from .validators import FileValidator


class MediaFile(AuditableModel):
    user = models.CharField(max_length=255)
    file_name = models.CharField(max_length=255)
    upload = models.FileField(
        upload_to="uploads/",
        validators=[
            FileValidator.validate_file_extension,
            FileValidator.validate_file_size,
        ],
    )
    thumbnail = models.FileField(upload_to="thumbnail/", blank=True, null=True)
    preview = models.FileField(upload_to="previews/", blank=True, null=True)
    original_size = models.FloatField(default=float, blank=True)
    new_size = models.FloatField(default=float, blank=True)
    compression_status = models.CharField(
        max_length=25,
        default=CompressionStatus.DEFAULT,
        choices=CompressionStatus.choices,
    )
    duration = models.CharField(max_length=20, blank=True, null=True)
    mimetype = models.CharField(max_length=50)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return self.file_name

    @staticmethod
    def convert_bytes(size: int, unit: Literal["kilo", "mega"] = "mega"):
        rates = {"kilo": 1000, "mega": 1_000_000}  # units in decimal
        result = size / rates.get(unit, "mega")
        formatted_result = f"{result:.2f}"
        return float(formatted_result)

    def url(self) -> str:
        if self.upload:
            return self.upload.storage.url(self.upload.name)
