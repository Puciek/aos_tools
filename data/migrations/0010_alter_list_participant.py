# Generated by Django 4.2.7 on 2023-11-18 06:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("data", "0009_participant_army_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="list",
            name="participant",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="list",
                to="data.participant",
            ),
        ),
    ]
