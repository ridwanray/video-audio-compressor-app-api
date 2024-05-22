from tempfile import NamedTemporaryFile

import boto3
from django.conf import settings

from .enums import CompressionStatus
from .helpers import MediaHelper
from .models import MediaFile

access_key = settings.AWS_ACCESS_KEY_ID
secret = settings.AWS_SECRET_ACCESS_KEY
bucket = settings.AWS_STORAGE_BUCKET_NAME

options = {"aws_access_key_id": access_key, "aws_secret_access_key": secret}


class S3Manager:

    def __init__(self):
        self.s3 = boto3.client("s3", **options)
        self.bucket_name = bucket

    def download_original_media_from_s3(
        self, temp_dir: str, key: str, media: MediaFile
    ) -> tuple[str, MediaFile]:
        try:

            with NamedTemporaryFile(dir=temp_dir, delete=False) as tmp_s3_file:
                self.s3.download_fileobj(self.bucket_name, key, tmp_s3_file)
                media.duration = MediaHelper.compute_duration(tmp_s3_file.name)
                media.compression_status = CompressionStatus.CONVERTING
                media.save(update_fields=["duration", "compression_status"])
                return tmp_s3_file.name, media
        except Exception as err:
            # TODO: add logging
            raise Exception("Error downloading from s3", key)

    def delete_original_file_from_s3(self, media_key: str):
        try:
            self.s3.delete_object(Bucket=self.bucket_name, Key=media_key)
        except Exception as e:
            # TODO: add logging
            print("An exception is captured in delete_object", str(e))
