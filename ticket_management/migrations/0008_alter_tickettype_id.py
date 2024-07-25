# Generated by Django 5.0.6 on 2024-07-25 09:27

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ticket_management", "0007_remove_tickettype_is_deleted"),
    ]

    operations = [
        migrations.AlterField(
            model_name="tickettype",
            name="id",
            field=models.UUIDField(
                default=uuid.uuid4,
                editable=False,
                primary_key=True,
                serialize=False,
                unique=True,
            ),
        ),
    ]