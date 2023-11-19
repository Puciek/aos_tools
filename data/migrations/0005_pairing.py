# Generated by Django 4.2.7 on 2023-11-17 20:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("data", "0004_event_rounds"),
    ]

    operations = [
        migrations.CreateModel(
            name="Pairing",
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
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("round", models.IntegerField()),
                ("player1_result", models.IntegerField(null=True)),
                ("player2_result", models.IntegerField(null=True)),
                ("player1_score", models.IntegerField(null=True)),
                ("player2_score", models.IntegerField(null=True)),
                (
                    "player1",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="player1",
                        to="data.participant",
                    ),
                ),
                (
                    "player1_list",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="player1_list",
                        to="data.list",
                    ),
                ),
                (
                    "player2",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="player2",
                        to="data.participant",
                    ),
                ),
                (
                    "player2_list",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="player2_list",
                        to="data.list",
                    ),
                ),
            ],
        ),
    ]
