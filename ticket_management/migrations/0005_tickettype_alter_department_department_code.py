# Generated by Django 5.0.6 on 2024-07-25 07:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ticket_management", "0004_alter_department_department_code_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="TicketType",
            fields=[
                ("id", models.UUIDField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=255)),
                ("is_active", models.BooleanField(default=False)),
                ("created_by", models.IntegerField(null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_by", models.IntegerField(null=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
            ],
            options={
                "db_table": "ticket_type",
            },
        ),
        migrations.AlterField(
            model_name="department",
            name="department_code",
            field=models.CharField(max_length=150),
        ),
    ]