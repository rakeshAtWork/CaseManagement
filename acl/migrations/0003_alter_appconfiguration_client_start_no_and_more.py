# Generated by Django 5.0.6 on 2024-08-05 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("acl", "0002_alter_appconfiguration_options_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="appconfiguration",
            name="client_start_no",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="appconfiguration",
            name="project_start_no",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="appconfiguration",
            name="ticket_start_no",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]