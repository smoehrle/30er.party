from __future__ import annotations
import uuid
from pathlib import Path

from django.db import models
from django.contrib import admin


def generate_image_path(instance: PartyImage, image_name: str):
    """Generate a dynamic path for images in the media folder"""
    file_extension = Path(image_name).suffix
    new_name = str(uuid.uuid4()) + file_extension
    return new_name


class PartyImage(models.Model):
    image = models.ImageField(upload_to=generate_image_path)
    is_ready = models.BooleanField(default=False, null=False, blank=False)
    created_on = models.DateTimeField(auto_now_add=True)

@admin.register(PartyImage)
class PartyImageAdmin(admin.ModelAdmin):
    pass
