from celery import shared_task
from celery.utils.log import get_task_logger
from website.models import PartyImage
from django.core.files.storage import default_storage
from pathlib import Path
from PIL import Image, ImageOps
import io

logger = get_task_logger(__name__)


@shared_task
def image_processor(image_id: int):

    try:
        party_image = PartyImage.objects.get(id=image_id)
    except PartyImage.DoesNotExist:
        logger.error("PartyImage with id=%s does not exist", image_id)
        return

    path = Path(party_image.image.name)
    with default_storage.open(path, "rb+") as file:
        with Image.open(file) as image_file:
            # If orientation is specified in exif, this will fix the image
            # even after the exif data is removed.
            new_image = ImageOps.exif_transpose(image_file)

            # Save original image as jpeg
            new_image.format = "JPEG"
            jpeg_path = party_image.jpeg_path(party_image.image.name)
            write_image(jpeg_path, new_image, quality=70)

            # Thumbnail
            new_image.thumbnail((400, 400), Image.Resampling.LANCZOS)
            thumb_path = party_image.thumbnail_path(party_image.image.name)
            write_image(thumb_path, new_image, quality=70)

    # DB UPDATE
    party_image.is_ready = True
    party_image.image.name = str(jpeg_path)
    party_image.save(update_fields=["is_ready", "image"])


def write_image(path: Path, image: Image.Image, quality: int):
    """Write an image to storage"""
    with io.BytesIO() as memfile:
        image.save(memfile, image.format, quality=quality, exif=Image.Exif())
        default_storage.save(path, memfile)
