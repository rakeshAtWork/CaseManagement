# Generated by Django 5.0.6 on 2024-07-18 04:10

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Application",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("status", models.BooleanField(default=False)),
                ("code", models.CharField(blank=True, max_length=25, null=True)),
                ("name", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "contact_name",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "contact_email",
                    models.EmailField(blank=True, max_length=254, null=True),
                ),
                (
                    "contact_number",
                    models.CharField(blank=True, max_length=20, null=True),
                ),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("created_by", models.PositiveIntegerField()),
                ("modified_on", models.DateTimeField(blank=True, null=True)),
                ("modified_by", models.PositiveIntegerField(null=True)),
                ("is_delete", models.BooleanField(default=False)),
            ],
            options={
                "db_table": "APPLICATION",
                "ordering": ["created_on"],
            },
        ),
        migrations.CreateModel(
            name="BusinessUnit",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("client_id", models.CharField(max_length=255, null=True)),
                ("code", models.CharField(max_length=25)),
                ("name", models.CharField(max_length=255)),
                ("contact_name", models.CharField(max_length=255)),
                (
                    "contact_email",
                    models.EmailField(blank=True, max_length=254, null=True),
                ),
                ("contact_number", models.CharField(max_length=15)),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("created_by", models.PositiveIntegerField()),
                ("modified_on", models.DateTimeField(blank=True, null=True)),
                ("modified_by", models.PositiveIntegerField(null=True)),
                ("is_delete", models.BooleanField(default=False)),
                ("status", models.BooleanField(default=True)),
            ],
            options={
                "db_table": "BUSINESS_UNIT",
                "ordering": ["created_on"],
            },
        ),
        migrations.CreateModel(
            name="Client",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("status", models.BooleanField(default=False)),
                ("code", models.CharField(max_length=25)),
                ("name", models.CharField(max_length=255)),
                ("contact_name", models.CharField(max_length=255)),
                (
                    "contact_email",
                    models.EmailField(blank=True, max_length=254, null=True),
                ),
                ("contact_number", models.CharField(max_length=15)),
                ("is_delete", models.BooleanField(default=False)),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("created_by", models.PositiveIntegerField()),
                ("modified_on", models.DateTimeField(blank=True, null=True)),
                ("modified_by", models.PositiveIntegerField(null=True)),
            ],
            options={
                "db_table": "CLIENT",
                "ordering": ["created_on"],
            },
        ),
        migrations.CreateModel(
            name="Customer",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("client_id", models.CharField(blank=True, max_length=255, null=True)),
                ("status", models.BooleanField(default=False)),
                ("code", models.CharField(max_length=25)),
                ("name", models.CharField(max_length=255)),
                ("contact_name", models.CharField(max_length=255)),
                (
                    "contact_email",
                    models.EmailField(blank=True, max_length=254, null=True),
                ),
                ("contact_number", models.CharField(max_length=15)),
                (
                    "retention_period",
                    models.PositiveIntegerField(blank=True, null=True),
                ),
                (
                    "disposal_action",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("ARCHIVE", "ARCHIVE"),
                            ("DELETE", "DELETE"),
                            ("REVIEW", "REVIEW"),
                        ],
                        max_length=50,
                        null=True,
                    ),
                ),
                (
                    "disposal_notification_period",
                    models.PositiveIntegerField(blank=True, null=True),
                ),
                ("is_delete", models.BooleanField(default=False)),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("created_by", models.PositiveIntegerField()),
                ("modified_on", models.DateTimeField(blank=True, null=True)),
                ("modified_by", models.PositiveIntegerField(null=True)),
            ],
            options={
                "db_table": "CUSTOMER",
                "ordering": ["created_on"],
            },
        ),
        migrations.CreateModel(
            name="FileType",
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
                ("status", models.BooleanField(default=False)),
                ("file_type", models.CharField(max_length=255)),
                ("file_extension", models.CharField(max_length=25)),
                ("max_file_size", models.PositiveIntegerField()),
                (
                    "file_description",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("created_by", models.PositiveIntegerField()),
                ("modified_on", models.DateTimeField(blank=True, null=True)),
                ("modified_by", models.PositiveIntegerField(null=True)),
                ("is_delete", models.BooleanField(default=False)),
            ],
            options={
                "db_table": "FILE_TYPE",
                "ordering": ["created_on"],
            },
        ),
        migrations.CreateModel(
            name="Vendor",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "customer_id",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("status", models.BooleanField(default=False)),
                ("code", models.CharField(max_length=255)),
                ("name", models.CharField(max_length=255)),
                (
                    "contact_name",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "contact_email",
                    models.EmailField(blank=True, max_length=254, null=True),
                ),
                ("contact_number", models.CharField(max_length=15)),
                (
                    "retention_period",
                    models.PositiveIntegerField(blank=True, null=True),
                ),
                (
                    "disposal_action",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("ARCHIVE", "ARCHIVE"),
                            ("DELETE", "DELETE"),
                            ("REVIEW", "REVIEW"),
                        ],
                        max_length=50,
                        null=True,
                    ),
                ),
                (
                    "disposal_notification_period",
                    models.PositiveIntegerField(blank=True, null=True),
                ),
                ("is_delete", models.BooleanField(default=False)),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("created_by", models.PositiveIntegerField()),
                ("modified_on", models.DateTimeField(blank=True, null=True)),
                ("modified_by", models.PositiveIntegerField(null=True)),
            ],
            options={
                "db_table": "VENDOR",
                "ordering": ["created_on"],
            },
        ),
    ]
