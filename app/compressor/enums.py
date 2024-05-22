from django.db import models


class CompressionStatus(models.TextChoices):
    DEFAULT = ("PENDING", "PENDING")
    CONVERTING = ("CONVERTING", "CONVERTING")
    COMPLETED = ("COMPLETED", "COMPLETED")
    CANCELLED = ("CANCELLED", "CANCELLED")
