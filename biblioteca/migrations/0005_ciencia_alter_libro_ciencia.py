# Generated by Django 5.1 on 2024-10-04 18:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("biblioteca", "0004_alter_libro_descripcion"),
    ]

    operations = [
        migrations.CreateModel(
            name="Ciencia",
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
                ("nombre", models.CharField(max_length=255)),
                ("descripcion", models.TextField(blank=True, null=True)),
                ("estado", models.BooleanField(default=True)),
            ],
        ),
        migrations.AlterField(
            model_name="libro",
            name="ciencia",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="biblioteca.ciencia"
            ),
        ),
    ]
