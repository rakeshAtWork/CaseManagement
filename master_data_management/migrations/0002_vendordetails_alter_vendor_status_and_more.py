# Generated by Django 5.0.6 on 2024-08-01 11:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("master_data_management", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="VendorDetails",
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
                ("company_code", models.CharField(max_length=255)),
                ("company_name", models.CharField(max_length=255)),
                ("agent_number", models.CharField(max_length=255)),
                ("supplier_type", models.CharField(max_length=255)),
                ("currency", models.CharField(max_length=255)),
                ("terms_of_payment", models.CharField(max_length=255)),
                ("supplier_name", models.CharField(max_length=255)),
                ("siret_number", models.CharField(max_length=255)),
                ("vat_country_code", models.CharField(max_length=255)),
                ("orbis_id", models.CharField(max_length=255)),
                ("orbis_id_found", models.BooleanField(default=False)),
                ("address_line", models.CharField(max_length=255)),
                ("country", models.CharField(max_length=255)),
                ("postal_code", models.CharField(max_length=20)),
                ("town", models.CharField(max_length=255)),
                ("country_code", models.CharField(max_length=10)),
                ("swift_number", models.CharField(max_length=255)),
                ("is_prime_revenue", models.BooleanField(default=False)),
                ("created_by", models.PositiveIntegerField()),
                ("updated_by", models.PositiveIntegerField()),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("updated_on", models.DateTimeField(auto_now=True)),
                ("is_delete", models.BooleanField(default=False)),
            ],
            options={
                "db_table": "VENDOR_DETAILS",
            },
        ),
        migrations.AlterField(
            model_name="vendor",
            name="status",
            field=models.IntegerField(default=False),
        ),
        migrations.CreateModel(
            name="SupplierContactDetails",
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
                ("contact_person", models.CharField(max_length=255)),
                ("main_phone_number", models.CharField(max_length=20)),
                ("main_email_id", models.EmailField(max_length=254)),
                (
                    "finance_phone_number",
                    models.CharField(blank=True, max_length=20, null=True),
                ),
                (
                    "finance_email_id",
                    models.EmailField(blank=True, max_length=254, null=True),
                ),
                (
                    "remittance_email_id",
                    models.EmailField(blank=True, max_length=254, null=True),
                ),
                (
                    "email_for_receiving_po",
                    models.EmailField(blank=True, max_length=254, null=True),
                ),
                (
                    "email_id_for_quote",
                    models.EmailField(blank=True, max_length=254, null=True),
                ),
                ("created_by", models.PositiveIntegerField()),
                ("updated_by", models.PositiveIntegerField()),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("updated_on", models.DateTimeField(auto_now=True)),
                ("is_delete", models.BooleanField(default=False)),
                (
                    "vendor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="contact_details",
                        to="master_data_management.vendordetails",
                    ),
                ),
            ],
            options={
                "db_table": "SUPPLIER_CONTACT_DETAILS",
            },
        ),
        migrations.CreateModel(
            name="D365FOSetup",
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
                ("sales_tax_group", models.CharField(max_length=255)),
                ("vendor_group", models.CharField(max_length=255)),
                ("payment_method", models.CharField(max_length=255)),
                ("business_unit", models.CharField(max_length=255)),
                ("inter_company", models.BooleanField(default=False)),
                ("vendor_hold", models.BooleanField(default=False)),
                ("source_system", models.CharField(max_length=255)),
                ("source_system_supplier_reference", models.CharField(max_length=255)),
                ("d365fo_id", models.CharField(max_length=255)),
                ("fs_ticket_number", models.CharField(max_length=255)),
                ("allow_false_duplicates", models.BooleanField(default=False)),
                ("additional_comments", models.TextField(blank=True, null=True)),
                ("created_by", models.PositiveIntegerField()),
                ("updated_by", models.PositiveIntegerField()),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("updated_on", models.DateTimeField(auto_now=True)),
                ("is_delete", models.BooleanField(default=False)),
                (
                    "vendor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="d365fo_setup",
                        to="master_data_management.vendordetails",
                    ),
                ),
            ],
            options={
                "db_table": "D365FO_SETUP",
            },
        ),
        migrations.CreateModel(
            name="CPPSanctionAssessment",
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
                ("cfra_score", models.CharField(max_length=255)),
                ("cfra_portfolio_id", models.CharField(max_length=255)),
                ("cfra_score_card", models.CharField(max_length=255)),
                ("cfra_assessment", models.CharField(max_length=255)),
                ("created_by", models.PositiveIntegerField()),
                ("updated_by", models.PositiveIntegerField()),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("updated_on", models.DateTimeField(auto_now=True)),
                ("is_delete", models.BooleanField(default=False)),
                (
                    "vendor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="sanction_assessments",
                        to="master_data_management.vendordetails",
                    ),
                ),
            ],
            options={
                "db_table": "CPP_SANCTION_ASSESSMENT",
            },
        ),
        migrations.CreateModel(
            name="CompanyInfoForValidation",
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
                ("orbis_supplier", models.CharField(max_length=255)),
                ("orbis_bvd", models.CharField(max_length=255)),
                ("vat_supplier", models.CharField(max_length=255)),
                ("vat_validity", models.CharField(max_length=255)),
                ("vat_validity_date", models.DateField()),
                ("created_by", models.PositiveIntegerField()),
                ("updated_by", models.PositiveIntegerField()),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("updated_on", models.DateTimeField(auto_now=True)),
                ("is_delete", models.BooleanField(default=False)),
                (
                    "vendor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="validation_info",
                        to="master_data_management.vendordetails",
                    ),
                ),
            ],
            options={
                "db_table": "COMPANY_INFO_FOR_VALIDATION",
            },
        ),
        migrations.CreateModel(
            name="AccountType",
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
                (
                    "account_type",
                    models.CharField(
                        choices=[("IBAN", "IBAN"), ("Domestic", "Domestic")],
                        max_length=10,
                    ),
                ),
                ("created_by", models.PositiveIntegerField()),
                ("updated_by", models.PositiveIntegerField()),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("updated_on", models.DateTimeField(auto_now=True)),
                ("is_delete", models.BooleanField(default=False)),
                (
                    "vendor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="account_types",
                        to="master_data_management.vendordetails",
                    ),
                ),
            ],
            options={
                "db_table": "ACCOUNT_TYPE",
            },
        ),
    ]