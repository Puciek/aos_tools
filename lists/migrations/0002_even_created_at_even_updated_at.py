# Generated by Django 4.2.7 on 2023-11-17 00:41

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("lists", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="even",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="even",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
    ]
