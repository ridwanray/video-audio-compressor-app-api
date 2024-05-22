from os import stat
from os.path import basename
from tempfile import TemporaryDirectory
from uuid import UUID

from celery import shared_task
from django.core.files.base import File
from django.utils.crypto import get_random_string

from .enums import CompressionStatus
from .helpers import MediaHelper
from .models import MediaFile
from .utils import S3Manager


@shared_task(name="remove_s3_original_media")
def delete_original_media(media_key: str):
    S3Manager().delete_original_file_from_s3(media_key)


@shared_task()
def compress_media_upload(upload_name: str, media_id: UUID, filetype: str):
    # uploads/sample.mp4
    base_name: str = basename(upload_name)  # sample.mp4
    file_name: str = base_name.split(".")[0]
    directory_name: str = file_name + get_random_string(8)
    media_obj = MediaFile.objects.get(id=media_id)

    try:

        with TemporaryDirectory(prefix=directory_name) as temp_compression_dir:
            media_key = f"media/{upload_name}"
            downloaded_file_path, media = S3Manager().download_original_media_from_s3(
                temp_dir=temp_compression_dir, key=media_key, media=media_obj
            )

            match filetype:
                case "video":
                    with open(
                        MediaHelper.generate_video_thumbnail(
                            downloaded_file_path, temp_compression_dir
                        ),
                        "rb",
                    ) as thumbnail_file:
                        media.thumbnail = File(
                            thumbnail_file, basename(thumbnail_file.name)
                        )
                        media.save()

                    with open(
                        MediaHelper.generate_video_preview(
                            downloaded_file_path, file_name, temp_compression_dir
                        ),
                        "rb",
                    ) as video_preview_file:
                        media.preview = File(
                            video_preview_file, basename(video_preview_file.name)
                        )
                        media.save()

                    compressed_video_path = MediaHelper.compress_video(
                        downloaded_file_path, file_name, temp_compression_dir
                    )

                    with open(compressed_video_path, "rb") as compressed_video:
                        media.upload = File(
                            compressed_video, name=basename(compressed_video.name)
                        )
                        media.new_size = MediaFile.convert_bytes(
                            stat(compressed_video_path).st_size, "mega"
                        )
                        media.save()

                case "audio":
                    compressed_audio_path = MediaHelper.compress_audio(
                        downloaded_file_path, file_name, temp_compression_dir
                    )
                    with open(compressed_audio_path, "rb") as compressed_audio:
                        media.upload = File(
                            compressed_audio, basename(compressed_audio.name)
                        )
                        media.new_size = MediaFile.convert_bytes(
                            stat(compressed_audio_path).st_size, "mega"
                        )
                        media.save()

                case _:
                    raise Exception(f"Unsupported media type detected: {filetype}")

            media_obj.compression_status = CompressionStatus.COMPLETED
    except Exception as err:
        # TODO: add logging
        media_obj.compression_status = CompressionStatus.CANCELLED
        raise Exception(f"Conversion and upload failed: {err}")
    finally:
        media_obj.save(update_fields=["compression_status"])
        delete_original_media.delay(media_key)
