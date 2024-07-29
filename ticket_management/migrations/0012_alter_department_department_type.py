# Generated by Django 5.0.6 on 2024-07-29 08:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ticket_management", "0011_alter_department_department_type"),
    ]

    operations = [
        migrations.AlterField(
            model_name="department",
            name="department_type",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="categories",
                to="ticket_management.category",
            ),
        ),
    ]