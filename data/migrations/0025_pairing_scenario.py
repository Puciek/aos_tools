# Generated by Django 4.2.10 on 2024-02-11 02:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0024_auto_20240207_2254'),
    ]

    operations = [
        migrations.AddField(
            model_name='pairing',
            name='scenario',
            field=models.CharField(max_length=255, null=True),
        ),
    ]