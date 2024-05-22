import os

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import UploadedFile

VALID_EXTENSIONS = [
    ".mp3",  # audio
    ".wav",
    ".aac",
    ".mp4",  # video
    ".mov",
    ".mkv",
    ".webm",
]


class FileValidator:

    @staticmethod
    def validate_file_extension(file_object: UploadedFile):
        ext: str = os.path.splitext(file_object.name)[1]
        if ext.lower() not in VALID_EXTENSIONS:
            allowable_exts = ", ".join(VALID_EXTENSIONS)
            raise ValidationError(
                f"Your file must be one of the following: {allowable_exts}"
            )

    @staticmethod
    def validate_file_size(file_object: UploadedFile):
        file_size = file_object.size
        if file_size > settings.MAX_UPLOAD_SIZE:
            max_allowable_mb = settings.MAX_UPLOAD_SIZE / 1_048_576
            raise ValidationError(f"Max allowable file size is {max_allowable_mb}MB")
