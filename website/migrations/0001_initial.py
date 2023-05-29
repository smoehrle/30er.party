# Generated by Django 4.2 on 2023-05-29 19:43

from django.db import migrations, models
import website.models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="PartyImage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "image",
                    models.ImageField(upload_to=website.models.generate_image_path),
                ),
                ("is_ready", models.BooleanField(default=False)),
                ("created_on", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]