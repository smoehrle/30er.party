# Generated by Django 4.2 on 2023-06-02 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0004_alter_playresult_points'),
    ]

    operations = [
        migrations.AddField(
            model_name='playgame',
            name='finished',
            field=models.BooleanField(default=False),
        ),
    ]
