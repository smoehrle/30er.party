from __future__ import annotations
from pathlib import Path
from datetime import datetime

from django.db import models
from django.contrib import admin

from pathlib import Path


def generate_image_path(instance: models.Model, image_name: str):
    """Generate a dynamic path for images in the media folder"""
    file_extension = Path(image_name).suffix
    datetime_str = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    return f"orig/{datetime_str}{file_extension}"


class PartyImage(models.Model):
    image = models.ImageField(upload_to=generate_image_path)
    is_ready = models.BooleanField(default=False, null=False, blank=False)
    created_on = models.DateTimeField(auto_now_add=True)

    @property
    def thumb_url(self):
        return self.thumbnail_path(self.image.url)

    def thumbnail_path(self, orig_path: str):
        """Return the url of the thumbnail"""
        path = Path(orig_path)
        thumb_dir = path.parent.parent / "thumbs"
        return thumb_dir / path.with_suffix(".jpeg").name

    @property
    def jpeg_url(self):
        return self.jpeg_path(self.image.url)

    def jpeg_path(self, orig_path: str):
        """Return the url of the normalized jpeg"""
        path = Path(orig_path)
        thumb_dir = path.parent.parent / "jpeg"
        return thumb_dir / path.with_suffix(".jpeg").name


@admin.register(PartyImage)
class PartyImageAdmin(admin.ModelAdmin):
    pass
