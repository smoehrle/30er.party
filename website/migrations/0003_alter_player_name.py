# Generated by Django 4.2 on 2023-06-01 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_game_player_playgame_playresult'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='name',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
