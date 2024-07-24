# Generated by Django 5.0.6 on 2024-07-18 04:10

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="CustomUser",
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
                ("password", models.CharField(max_length=128, verbose_name="password")),
                ("is_staff", models.BooleanField(default=False)),
                ("is_superuser", models.BooleanField(default=False)),
                ("email", models.EmailField(max_length=254, unique=True)),
                ("first_name", models.CharField(max_length=15)),
                ("last_name", models.CharField(max_length=15, null=True)),
                ("client_id", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "phone_number",
                    models.CharField(blank=True, max_length=15, null=True),
                ),
                (
                    "organisation_name",
                    models.CharField(blank=True, max_length=15, null=True),
                ),
                ("timezone", models.CharField(blank=True, max_length=50, null=True)),
                ("country", models.CharField(blank=True, max_length=50, null=True)),
                ("is_active", models.BooleanField(default=False)),
                ("is_delete", models.BooleanField(default=False)),
                ("is_application", models.BooleanField(default=False)),
                ("last_login", models.DateTimeField(blank=True, null=True)),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("created_by", models.IntegerField(null=True)),
                ("modified_on", models.DateTimeField(null=True)),
                ("modified_by", models.IntegerField(null=True)),
            ],
            options={
                "db_table": "CUSTOM_USER",
                "ordering": ["first_name"],
            },
        ),
        migrations.CreateModel(
            name="TokenModule",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                ("expiry_days", models.PositiveIntegerField(default=10)),
                ("expiry_time", models.DateTimeField(null=True)),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("APP_TOKEN", "APP_TOKEN"),
                            ("LOGIN_TOKEN", "LOGIN_TOKEN"),
                        ],
                        default="APP_TOKEN",
                        max_length=255,
                    ),
                ),
                (
                    "primary_token",
                    models.CharField(blank=True, max_length=120, null=True),
                ),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("created_by", models.IntegerField(null=True)),
                ("modified_on", models.DateTimeField(null=True)),
                ("modified_by", models.IntegerField(null=True)),
                (
                    "user_id",
                    models.OneToOneField(
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="token_user_id",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "db_table": "TOKEN_MANAGEMENT",
                "ordering": ["-created_on"],
            },
        ),
    ]