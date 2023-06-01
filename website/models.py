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


class Player(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f'[{self.id}] {self.name}'

class Game(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=2000, blank=True)

    def __str__(self):
        return f'[{self.id}] {self.name}'

class PlayGame(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    participants = models.ManyToManyField(Player)
    time_stamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'[{self.id}] {self.time_stamp}: with {len(self.participants)} player'

class PlayResult(models.Model):
    play_game = models.ForeignKey(PlayGame, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    is_winner = models.BooleanField(default=False)
    points = models.ImageField(null=True, blank=True)

    def __str__(self):
        return f'[{self.id}] {self.play_game.game.name} {self.player.name} {"Winner" if self.is_winner else "Looser"}'

@admin.register(PartyImage)
class PartyImageAdmin(admin.ModelAdmin):
    pass

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    pass

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    pass

@admin.register(PlayGame)
class PlayGameAdmin(admin.ModelAdmin):
    pass

@admin.register(PlayResult)
class PlayResultAdmin(admin.ModelAdmin):
    pass
