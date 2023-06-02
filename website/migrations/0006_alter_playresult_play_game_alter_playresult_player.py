# Generated by Django 4.2 on 2023-06-02 17:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0005_playgame_finished'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playresult',
            name='play_game',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='game_result', to='website.playgame'),
        ),
        migrations.AlterField(
            model_name='playresult',
            name='player',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='player_result', to='website.player'),
        ),
    ]