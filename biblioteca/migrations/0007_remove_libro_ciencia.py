# Generated by Django 5.1 on 2024-10-04 18:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("biblioteca", "0006_alter_libro_ciencia"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="libro",
            name="ciencia",
        ),
    ]
