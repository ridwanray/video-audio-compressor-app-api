from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import MediaFile
from .tasks import compress_media_upload


@receiver(post_save, sender=MediaFile)
def initiate_media_compression(sender, instance: MediaFile, created, **kwargs):

    filetype = instance.mimetype.split("/")[0]  # video/mp4, audio/mp3
    if created and filetype in ["audio", "video"]:
        compress_media_upload.delay(instance.upload.name, instance.id, filetype)
