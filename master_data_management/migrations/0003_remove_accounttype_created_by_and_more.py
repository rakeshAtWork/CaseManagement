# Generated by Django 5.0.6 on 2024-08-02 06:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("master_data_management", "0002_vendordetails_alter_vendor_status_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="accounttype",
            name="created_by",
        ),
        migrations.RemoveField(
            model_name="accounttype",
            name="created_on",
        ),
        migrations.RemoveField(
            model_name="accounttype",
            name="updated_by",
        ),
        migrations.RemoveField(
            model_name="accounttype",
            name="updated_on",
        ),
        migrations.RemoveField(
            model_name="companyinfoforvalidation",
            name="created_by",
        ),
        migrations.RemoveField(
            model_name="companyinfoforvalidation",
            name="created_on",
        ),
        migrations.RemoveField(
            model_name="companyinfoforvalidation",
            name="updated_by",
        ),
        migrations.RemoveField(
            model_name="companyinfoforvalidation",
            name="updated_on",
        ),
        migrations.RemoveField(
            model_name="cppsanctionassessment",
            name="created_by",
        ),
        migrations.RemoveField(
            model_name="cppsanctionassessment",
            name="created_on",
        ),
        migrations.RemoveField(
            model_name="cppsanctionassessment",
            name="updated_by",
        ),
        migrations.RemoveField(
            model_name="cppsanctionassessment",
            name="updated_on",
        ),
        migrations.RemoveField(
            model_name="d365fosetup",
            name="created_by",
        ),
        migrations.RemoveField(
            model_name="d365fosetup",
            name="created_on",
        ),
        migrations.RemoveField(
            model_name="d365fosetup",
            name="updated_by",
        ),
        migrations.RemoveField(
            model_name="d365fosetup",
            name="updated_on",
        ),
        migrations.RemoveField(
            model_name="suppliercontactdetails",
            name="created_by",
        ),
        migrations.RemoveField(
            model_name="suppliercontactdetails",
            name="created_on",
        ),
        migrations.RemoveField(
            model_name="suppliercontactdetails",
            name="updated_by",
        ),
        migrations.RemoveField(
            model_name="suppliercontactdetails",
            name="updated_on",
        ),
        migrations.AlterField(
            model_name="accounttype",
            name="vendor",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="account_types",
                to="master_data_management.vendordetails",
            ),
        ),
        migrations.AlterField(
            model_name="companyinfoforvalidation",
            name="vendor",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="validation_info",
                to="master_data_management.vendordetails",
            ),
        ),
        migrations.AlterField(
            model_name="cppsanctionassessment",
            name="vendor",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="sanction_assessments",
                to="master_data_management.vendordetails",
            ),
        ),
        migrations.AlterField(
            model_name="d365fosetup",
            name="vendor",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="d365fo_setup_vendor",
                to="master_data_management.vendordetails",
            ),
        ),
        migrations.AlterField(
            model_name="suppliercontactdetails",
            name="vendor",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="contact_details",
                to="master_data_management.vendordetails",
            ),
        ),
    ]