# Generated by Django 4.2 on 2023-06-01 20:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(blank=True, max_length=2000)),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='PlayGame',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_stamp', models.DateTimeField(auto_now_add=True)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.game')),
                ('participants', models.ManyToManyField(to='website.player')),
            ],
        ),
        migrations.CreateModel(
            name='PlayResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_winner', models.BooleanField(default=False)),
                ('points', models.ImageField(blank=True, null=True, upload_to='')),
                ('play_game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.playgame')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.player')),
            ],
        ),
    ]
