# Generated by Django 4.2.7 on 2023-11-17 20:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("data", "0007_pairing_source_id_pairing_source_json"),
    ]

    operations = [
        migrations.AlterField(
            model_name="pairing",
            name="player1",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="player1",
                to="data.participant",
            ),
        ),
        migrations.AlterField(
            model_name="pairing",
            name="player2",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="player2",
                to="data.participant",
            ),
        ),
    ]
