from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from rest_framework import serializers

from user_management.models import CustomUser
from .models import (Currency, Country,
                     Category,
                     Department, UserDepartment, Status, EmailTemplate, UserStatus, StatusField, ActivityLog,
                     EmailTemplateType,
                     LineOfBusiness, LegalEntity, Vendor)

User = get_user_model()


# class FileTypeSerializers(serializers.ModelSerializer):
#     class Meta:
#         model = FileType
#         fields = (
#             "id", "status", "file_type", "file_extension", "max_file_size", "file_description", "created_by",
#             "modified_by", "created_on", "modified_on",)
#         read_only_fields = ("created_by", "modified_by", "created_on", "modified_on")
#
#     def create(self, validated_data):
#         try:
#             file_extension = validated_data.get('file_extension').lower()
#
#             regex_validator = RegexValidator(
#                 regex=r'^[a-zA-Z0-9]+$',
#                 message="File extension should not contain any special characters"
#             )
#             regex_validator(file_extension)
#
#             if FileType.objects.filter(file_extension__iexact=file_extension).exists():
#                 raise serializers.ValidationError("File extension name should be unique")
#             instance = super(FileTypeSerializers, self).create(validated_data)
#             return instance
#         except serializers.ValidationError as ve:
#             raise serializers.ValidationError(ve.detail)
#         except Exception as ee:
#             raise serializers.ValidationError(str(ee))
#
#
# class FileTypeReadSerializer(serializers.ModelSerializer):
#     """
#     Serializer for reading FileType data.
#     """
#
#     class Meta:
#         model = FileType
#         fields = '__all__'
#
#
# class FileTypeFilterSerializer(serializers.ModelSerializer):
#     """
#     Serializer for filtering FileType records.
#     """
#     status = serializers.BooleanField(required=False)
#     file_type = serializers.CharField(required=False, allow_blank=True, allow_null=True)
#     file_extension = serializers.CharField(required=False, allow_blank=True, allow_null=True)
#     is_delete = serializers.BooleanField(required=False)
#     order_by = serializers.CharField(required=False, allow_blank=True, allow_null=True, write_only=True)
#     order_type = serializers.CharField(required=False, allow_blank=True, allow_null=True, write_only=True)
#     page = serializers.IntegerField(required=False, write_only=True, allow_null=True)
#     page_size = serializers.IntegerField(required=False, write_only=True, allow_null=True)
#
#     class Meta:
#         model = FileType
#         fields = (
#             'status', 'file_type', 'file_extension', 'is_delete',
#             'order_by', 'order_type', 'page', 'page_size'
#         )


# class ClientSerializers(serializers.ModelSerializer):
#     class Meta:
#         model = Client
#         fields = (
#             "id", "status", "code", "name", "contact_name", "contact_email", "contact_number", "is_delete",
#             "created_by", "modified_by", "created_on", "modified_on")
#         read_only_fields = ("created_by", "modified_by", "created_on", "modified_on")
#
#     def create(self, validated_data):
#         try:
#             name = validated_data.get('name').lower()
#             code = validated_data.get('code').lower()
#
#             if Client.objects.filter(name__iexact=name).exists():
#                 raise serializers.ValidationError("Client name should be unique")
#             if Client.objects.filter(code__iexact=code).exists():
#                 raise serializers.ValidationError("Client code should be unique")
#             instance = super(ClientSerializers, self).create(validated_data)
#             return instance
#         except serializers.ValidationError as ve:
#             raise serializers.ValidationError(ve.detail)
#         except Exception as ee:
#             raise serializers.ValidationError(str(ee))


# class ClientReadSerializers(serializers.ModelSerializer):
# created_by = serializers.SerializerMethodField(source='get_created_by', read_only=True)
# modified_by = serializers.SerializerMethodField(source='get_updated_by', read_only=True)

# class Meta:
#     model = Client
#     fields = (
#         "id", "status", "code", "name", "contact_name", "contact_email", "contact_number", "is_delete",
#         "created_by", "modified_by", "created_on", "modified_on")

# def get_updated_by(self, obj):
#     data = User.objects.filter(id=obj.modified_by).first()
#     if data:
#         return f"{data.first_name} {data.last_name}".strip()
#     else:
#         return None
#
# def get_created_by(self, obj):
#     data = User.objects.filter(id=obj.created_by).first()
#     if data:
#         return f"{data.first_name} {data.last_name}".strip()
#     else:
#         return None


# class ClientFilterSerializers(serializers.Serializer):
#     status = serializers.BooleanField(allow_null=True, required=False)
#     code = serializers.CharField(allow_null=True, allow_blank=True, required=False)
#     name = serializers.CharField(allow_null=True, allow_blank=True, required=False)
#     contact_name = serializers.CharField(allow_null=True, allow_blank=True, required=False)
#     contact_email = serializers.CharField(allow_null=True, allow_blank=True, required=False)
#     contact_number = serializers.CharField(allow_null=True, allow_blank=True, required=False)
#     is_delete = serializers.BooleanField(allow_null=True, required=False)
#     created_on = serializers.DateTimeField(allow_null=True, required=False)
#     created_by = serializers.IntegerField(allow_null=True, required=False)
#     modified_on = serializers.DateTimeField(allow_null=True, required=False)
#     modified_by = serializers.IntegerField(allow_null=True, required=False)
#     order_by = serializers.CharField(required=False, allow_blank=True, allow_null=True)
#     order_type = serializers.CharField(required=False, allow_blank=True, allow_null=True)
#     export = serializers.BooleanField(required=False, allow_null=True, default=False)
#     page = serializers.IntegerField(required=False, allow_null=True)
#     page_size = serializers.IntegerField(required=False, allow_null=True)
#
#
# class CustomerSerializers(serializers.ModelSerializer):
#     class Meta:
#         model = Customer
#         fields = (
#             "id",
#             "client_id", "status", "code", "name", "contact_name", "contact_email", "contact_number", "is_delete",
#             "retention_period", "disposal_action", "disposal_notification_period",
#             "created_by", "modified_by", "created_on", "modified_on")
#         read_only_fields = ("created_by", "modified_by", "created_on", "modified_on")
#
#     def create(self, validated_data):
#         try:
#             name = validated_data.get('name').lower()
#             code = validated_data.get('code').lower()
#
#             if Customer.objects.filter(name__iexact=name).exists():
#                 raise serializers.ValidationError("Customer name should be unique")
#             if Customer.objects.filter(code__iexact=code).exists():
#                 raise serializers.ValidationError("Customer code should be unique")
#             instance = super(CustomerSerializers, self).create(validated_data)
#             return instance
#
#         except Exception as ee:
#             raise serializers.ValidationError(str(ee))
#
#
# class CustomerReadSerializers(serializers.ModelSerializer):
#     class Meta:
#         model = Customer
#         fields = (
#             "id", "client_id", "status", "code", "name", "contact_name", "contact_email", "contact_number", "is_delete",
#             "retention_period", "disposal_action", "disposal_notification_period",
#             "created_by", "modified_by", "created_on", "modified_on")
#
#
# class CustomerFilterSerializers(serializers.Serializer):
#     status = serializers.BooleanField(allow_null=True, required=False)
#     client_id = serializers.CharField(allow_null=True, required=False)
#     code = serializers.CharField(allow_null=True, required=False)
#     name = serializers.CharField(allow_null=True, required=False)
#     contact_name = serializers.CharField(allow_null=True, required=False)
#     contact_email = serializers.CharField(allow_null=True, required=False)
#     contact_number = serializers.CharField(allow_null=True, required=False)
#     retention_period = serializers.IntegerField(allow_null=True, required=False)
#     disposal_action = serializers.CharField(allow_null=True, required=False)
#     disposal_notification_period = serializers.IntegerField(allow_null=True, required=False)
#     is_delete = serializers.BooleanField(allow_null=True, required=False)
#     created_on = serializers.DateTimeField(allow_null=True, required=False)
#     created_by = serializers.IntegerField(allow_null=True, required=False)
#     modified_on = serializers.DateTimeField(allow_null=True, required=False)
#     modified_by = serializers.IntegerField(allow_null=True, required=False)
#     order_by = serializers.CharField(required=False, allow_blank=True, allow_null=True)
#     order_type = serializers.CharField(required=False, allow_blank=True, allow_null=True)
#     export = serializers.BooleanField(required=False, allow_null=True, default=False)
#     page = serializers.IntegerField(required=False, allow_null=True)
#     page_size = serializers.IntegerField(required=False, allow_null=True)
#
#
# class BusinessUnitSerializers(serializers.ModelSerializer):
#     class Meta:
#         model = BusinessUnit
#         fields = (
#             "id", "client_id", "code", "name", "contact_name", "contact_email", "contact_number",
#             "created_by", "modified_by", "created_on", "modified_on", "is_delete", "status")
#         read_only_fields = ("created_by", "modified_by", "created_on", "modified_on")
#
#     def create(self, validated_data):
#         try:
#             name = validated_data.get('name').lower()
#             code = validated_data.get('code').lower()
#
#             if BusinessUnit.objects.filter(name__iexact=name).exists():
#                 raise serializers.ValidationError("Business Unit name should be unique")
#             if BusinessUnit.objects.filter(code__iexact=code).exists():
#                 raise serializers.ValidationError("Business Unit code should be unique")
#             instance = super(BusinessUnitSerializers, self).create(validated_data)
#             return instance
#         except serializers.ValidationError as ve:
#             raise serializers.ValidationError(ve.detail)
#         except Exception as ee:
#             raise serializers.ValidationError(str(ee))
#
#
# class BusinessUnitReadSerializers(serializers.ModelSerializer):
#     class Meta:
#         model = BusinessUnit
#         fields = (
#             "id", "client_id", "code", "name", "contact_name", "contact_email", "contact_number",
#             "created_by", "modified_by", "created_on", "modified_on", "is_delete", "status")
#
#     def get_modified_by(self, obj):
#         data = User.objects.filter(id=obj.modified_by).first()
#         if data:
#             return f"{data.first_name} {data.last_name}".strip()
#         else:
#             return None
#
#     def get_created_by(self, obj):
#         data = User.objects.filter(id=obj.created_by).first()
#         if data:
#             return f"{data.first_name} {data.last_name}".strip()
#         else:
#             return None
#
#
# class BusinessUnitFilterSerializers(serializers.Serializer):
#     status = serializers.BooleanField(required=False, allow_null=True)
#     client_id = serializers.CharField(allow_null=True, allow_blank=True, required=False)
#     is_delete = serializers.CharField(allow_null=True, allow_blank=True, required=False)
#     code = serializers.CharField(allow_null=True, allow_blank=True, required=False)
#     name = serializers.CharField(allow_null=True, allow_blank=True, required=False)
#     contact_name = serializers.CharField(allow_null=True, allow_blank=True, required=False)
#     contact_email = serializers.CharField(allow_null=True, allow_blank=True, required=False)
#     contact_number = serializers.CharField(allow_null=True, allow_blank=True, required=False)
#     created_on = serializers.DateTimeField(allow_null=True, required=False)
#     created_by = serializers.IntegerField(allow_null=True, required=False)
#     modified_on = serializers.DateTimeField(allow_null=True, required=False)
#     modified_by = serializers.IntegerField(allow_null=True, required=False)
#     order_by = serializers.CharField(required=False, allow_blank=True, allow_null=True)
#     order_type = serializers.CharField(required=False, allow_blank=True, allow_null=True)
#     page = serializers.IntegerField(required=False, allow_null=True)
#     page_size = serializers.IntegerField(required=False, allow_null=True)
#     export = serializers.BooleanField(required=False, allow_null=True, default=False)
#
#
# class VendorSerializers(serializers.ModelSerializer):
#     class Meta:
#         model = Vendor
#         fields = (
#             "id", "is_delete", "customer_id", "status", "code", "name", "contact_name", "contact_email",
#             "contact_number", "retention_period", "disposal_action", "disposal_notification_period",
#             "created_by", "modified_by", "created_on", "modified_on")
#         read_only_fields = ("created_by", "modified_by", "created_on", "modified_on")
#
#     def create(self, validated_data):
#         try:
#             name = validated_data.get('name').lower()
#             code = validated_data.get('code').lower()
#
#             if Vendor.objects.filter(name__iexact=name).exists():
#                 raise serializers.ValidationError("Vendor name should be unique")
#             if Vendor.objects.filter(code__iexact=code).exists():
#                 raise serializers.ValidationError("Vendor code should be unique")
#             instance = super(VendorSerializers, self).create(validated_data)
#             return instance
#
#         except Exception as ee:
#             raise serializers.ValidationError(str(ee))
#
#
# class VendorReadSerializers(serializers.ModelSerializer):
#     class Meta:
#         model = Vendor
#         fields = (
#             "id", "is_delete", "customer_id", "status", "code", "name", "contact_name", "contact_email",
#             "retention_period", "disposal_action", "disposal_notification_period",
#             "contact_number", "created_by", "modified_by", "created_on", "modified_on")
#
#
# class VendorFilterSerializers(serializers.Serializer):
#     customer_id = serializers.CharField(allow_null=True, required=False)
#     status = serializers.BooleanField(allow_null=True, required=False)
#     code = serializers.CharField(allow_null=True, allow_blank=True, required=False)
#     name = serializers.CharField(allow_null=True, allow_blank=True, required=False)
#     contact_name = serializers.CharField(allow_null=True, allow_blank=True, required=False)
#     contact_email = serializers.CharField(allow_null=True, allow_blank=True, required=False)
#     contact_number = serializers.CharField(allow_null=True, allow_blank=True, required=False)
#     retention_period = serializers.IntegerField(allow_null=True, required=False)
#     disposal_action = serializers.CharField(allow_null=True, allow_blank=True, required=False)
#     disposal_notification_period = serializers.IntegerField(allow_null=True, required=False)
#     is_delete = serializers.BooleanField(allow_null=True, required=False)
#     created_on = serializers.DateTimeField(allow_null=True, required=False)
#     created_by = serializers.IntegerField(allow_null=True, required=False)
#     modified_on = serializers.DateTimeField(allow_null=True, required=False)
#     modified_by = serializers.IntegerField(allow_null=True, required=False)
#     order_by = serializers.CharField(required=False, allow_blank=True, allow_null=True)
#     order_type = serializers.CharField(required=False, allow_blank=True, allow_null=True)
#     export = serializers.BooleanField(required=False, allow_null=True, default=False)
#     page = serializers.IntegerField(required=False, allow_null=True)
#     page_size = serializers.IntegerField(required=False, allow_null=True)
#
#
# class ApplicationSerializers(serializers.ModelSerializer):
#     class Meta:
#         model = Application
#         fields = (
#             "id", "status", "code", "name", "created_by", "modified_by", "created_on", "modified_on", "contact_name",
#             "contact_email", "contact_number", "status")
#         read_only_fields = ("created_by", "modified_by", "created_on", "modified_on")
#
#
# class ApplicationReadSerializers(serializers.ModelSerializer):
#     class Meta:
#         model = Application
#         fields = (
#             "id", "status", "code", "name", "created_by", "modified_by", "created_on", "modified_on",
#             "contact_name", "contact_email", "contact_number", "status")
#
#
# class ApplicationFilterSerializers(serializers.Serializer):
#     status = serializers.BooleanField(allow_null=True, required=False)
#     code = serializers.CharField(allow_null=True, allow_blank=True, required=False)
#     name = serializers.CharField(allow_null=True, allow_blank=True, required=False)
#     contact_name = serializers.CharField(allow_null=True, allow_blank=True, required=False)
#     contact_email = serializers.CharField(allow_null=True, allow_blank=True, required=False)
#     contact_number = serializers.CharField(allow_null=True, allow_blank=True, required=False)
#     created_on = serializers.DateTimeField(allow_null=True, required=False)
#     created_by = serializers.IntegerField(allow_null=True, required=False)
#     modified_on = serializers.DateTimeField(allow_null=True, required=False)
#     modified_by = serializers.IntegerField(allow_null=True, required=False)
#     order_by = serializers.CharField(required=False, allow_blank=True, allow_null=True)
#     order_type = serializers.CharField(required=False, allow_blank=True, allow_null=True)
#     export = serializers.BooleanField(required=False, allow_null=True, default=False)
#     page = serializers.IntegerField(required=False, allow_null=True)
#     page_size = serializers.IntegerField(required=False, allow_null=True)
#
#
# class AccountTypeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = AccountType
#         fields = ['account_type']
#
#
# class SupplierContactDetailsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = SupplierContactDetails
#         fields = ['id', 'contact_person', 'main_phone_number', 'main_email_id', 'finance_phone_number',
#                   'finance_email_id', 'remittance_email_id', 'email_for_receiving_po', 'email_id_for_quote']
#
#
# class VendorDetailsFilterSerializer(serializers.Serializer):
#     company_code = serializers.CharField(required=False, allow_blank=True)
#     company_name = serializers.CharField(required=False, allow_blank=True)
#     agent_number = serializers.CharField(required=False, allow_blank=True)
#     supplier_type = serializers.CharField(required=False, allow_blank=True)
#     currency = serializers.CharField(required=False, allow_blank=True)
#     terms_of_payment = serializers.CharField(required=False, allow_blank=True)
#     supplier_name = serializers.CharField(required=False, allow_blank=True)
#     siret_number = serializers.CharField(required=False, allow_blank=True)
#     vat_country_code = serializers.CharField(required=False, allow_blank=True)
#     orbis_id = serializers.CharField(required=False, allow_blank=True)
#     orbis_id_found = serializers.BooleanField(required=False)
#     address_line = serializers.CharField(required=False, allow_blank=True)
#     country = serializers.CharField(required=False, allow_blank=True)
#     postal_code = serializers.CharField(required=False, allow_blank=True)
#     town = serializers.CharField(required=False, allow_blank=True)
#     country_code = serializers.CharField(required=False, allow_blank=True)
#     swift_number = serializers.CharField(required=False, allow_blank=True)
#     is_prime_revenue = serializers.BooleanField(required=False)
#     created_by = serializers.IntegerField(required=False)
#     modified_by = serializers.IntegerField(required=False)
#     created_on = serializers.DateTimeField(required=False)
#     modified_on = serializers.DateTimeField(required=False)
#
#
# class D365FOSetupSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = D365FOSetup
#         fields = '__all__'  # Include all fields in the serializer
#         read_only_fields = ('created_by', 'modified_by', 'created_on', 'modified_on')
#
#     def update(self, instance, validated_data):
#         # You can add custom update logic here if needed
#         for attr, value in validated_data.items():
#             setattr(instance, attr, value)
#         instance.save()
#         return instance
#
#
# class CompanyInfoForValidationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CompanyInfoForValidation
#         fields = ['orbis_supplier', 'orbis_bvd', 'vat_supplier', 'vat_validity', 'vat_validity_date']
#
#
# class CPPSanctionAssessmentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CPPSanctionAssessment
#         fields = ['cfra_score', 'cfra_portfolio_id', 'cfra_score_card', 'cfra_assessment']
#
#
# class VendorDetailsSerializer(serializers.ModelSerializer):
#     account_type = AccountTypeSerializer()
#     supplier_contact_details = SupplierContactDetailsSerializer()
#     d365fo_setup = D365FOSetupSerializer()
#     company_info_for_validation = CompanyInfoForValidationSerializer()
#     cpp_sanction_assessment = CPPSanctionAssessmentSerializer()
#
#     class Meta:
#         model = VendorDetails
#         fields = '__all__'
#
#     def create(self, validated_data):
#         # Extract nested data
#         account_type_data = validated_data.pop('account_type', None)
#         supplier_contact_details_data = validated_data.pop('supplier_contact_details', None)
#         d365fo_setup_data = validated_data.pop('d365fo_setup', None)
#         company_info_for_validation_data = validated_data.pop('company_info_for_validation', None)
#         cpp_sanction_assessment_data = validated_data.pop('cpp_sanction_assessment', None)
#
#         # Create related instances and associate them with the VendorDetails instance
#         if account_type_data:
#             account_type_data = AccountType.objects.create(**account_type_data)
#
#         if supplier_contact_details_data:
#             supplier_contact_details_data = SupplierContactDetails.objects.create(**supplier_contact_details_data)
#
#         if d365fo_setup_data:
#             d365fo_setup_data = D365FOSetup.objects.create(**d365fo_setup_data)
#
#         if company_info_for_validation_data:
#             company_info_for_validation_data = CompanyInfoForValidation.objects.create(
#                 **company_info_for_validation_data)
#
#         if cpp_sanction_assessment_data:
#             cpp_sanction_assessment_data = CPPSanctionAssessment.objects.create(**cpp_sanction_assessment_data)
#
#         # Create the VendorDetails instance at last
#         vendor_details = VendorDetails.objects.create(d365fo_setup=d365fo_setup_data,
#                                                       supplier_contact_details=supplier_contact_details_data,
#                                                       account_type=account_type_data,
#                                                       company_info_for_validation=company_info_for_validation_data,
#                                                       cpp_sanction_assessment=cpp_sanction_assessment_data,
#                                                       **validated_data)
#
#         return vendor_details
#
#
# class UpdateVendorDetailsSerializer(serializers.ModelSerializer):
#     account_type = AccountTypeSerializer(required=False)
#     supplier_contact_details = SupplierContactDetailsSerializer(required=False)
#     d365fo_setup = D365FOSetupSerializer(required=False)
#     company_info_for_validation = CompanyInfoForValidationSerializer(required=False)
#     cpp_sanction_assessment = CPPSanctionAssessmentSerializer(required=False)
#
#     class Meta:
#         model = VendorDetails
#         fields = '__all__'
#
#     def update(self, instance, validated_data):
#         account_type_data = validated_data.pop('account_type', None)
#         supplier_contact_details_data = validated_data.pop('supplier_contact_details', None)
#         d365fo_setup_data = validated_data.pop('d365fo_setup', None)
#         company_info_for_validation_data = validated_data.pop('company_info_for_validation', None)
#         cpp_sanction_assessment_data = validated_data.pop('cpp_sanction_assessment', None)
#
#         # Update the main VendorDetails fields
#         for attr, value in validated_data.items():
#             setattr(instance, attr, value)
#         instance.save()
#
#         # Update nested fields
#         if account_type_data:
#             account_type_instance = instance.account
#
#
# class D365FOSetupFilterSerializer(serializers.ModelSerializer):
#     sales_tax_group = serializers.CharField(required=False, allow_blank=True, allow_null=True)
#     vendor_group = serializers.CharField(required=False, allow_blank=True, allow_null=True)
#     payment_method = serializers.CharField(required=False, allow_blank=True, allow_null=True)
#     business_unit = serializers.CharField(required=False, allow_blank=True, allow_null=True)
#     inter_company = serializers.BooleanField(required=False, allow_null=True)
#     vendor_hold = serializers.BooleanField(required=False, allow_null=True)
#     source_system = serializers.CharField(required=False, allow_blank=True, allow_null=True)
#     source_system_supplier_reference = serializers.CharField(required=False, allow_blank=True, allow_null=True)
#     d365fo_id = serializers.CharField(required=False, allow_blank=True, allow_null=True)
#     fs_ticket_number = serializers.CharField(required=False, allow_blank=True, allow_null=True)
#     allow_false_duplicates = serializers.BooleanField(required=False, allow_null=True)
#     additional_comments = serializers.CharField(required=False, allow_blank=True, allow_null=True)
#     order_by = serializers.CharField(required=False, allow_blank=True, allow_null=True, write_only=True)
#     order_type = serializers.CharField(required=False, allow_blank=True, allow_null=True, write_only=True)
#     page = serializers.IntegerField(required=False, write_only=True, allow_null=True)
#     page_size = serializers.IntegerField(required=False, write_only=True, allow_null=True)
#
#     class Meta:
#         model = D365FOSetup
#         fields = ('sales_tax_group', 'vendor_group', 'payment_method', 'business_unit', 'inter_company',
#                   'vendor_hold', 'source_system', 'source_system_supplier_reference', 'd365fo_id',
#                   'fs_ticket_number', 'allow_false_duplicates', 'additional_comments', 'order_by',
#                   'order_type', 'page', 'page_size')
#
#
# class D365FOSetupReadSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = D365FOSetup
#         fields = ('id', 'sales_tax_group', 'vendor_group', 'payment_method', 'business_unit',
#                   'inter_company', 'vendor_hold', 'source_system', 'source_system_supplier_reference',
#                   'd365fo_id', 'fs_ticket_number', 'allow_false_duplicates', 'additional_comments',
#                   'created_by', 'modified_by', 'created_on', 'modified_on')
#         read_only_fields = ('created_by', 'modified_by', 'created_on', 'modified_on')
#
#
# class SupplierContactDetailsFilterSerializer(serializers.ModelSerializer):
#     contact_person = serializers.CharField(required=False, allow_blank=True, allow_null=True)
#     main_phone_number = serializers.CharField(required=False, allow_blank=True, allow_null=True)
#     main_email_id = serializers.EmailField(required=False, allow_blank=True, allow_null=True)
#     finance_phone_number = serializers.CharField(required=False, allow_blank=True, allow_null=True)
#     finance_email_id = serializers.EmailField(required=False, allow_blank=True, allow_null=True)
#     remittance_email_id = serializers.EmailField(required=False, allow_blank=True, allow_null=True)
#     email_for_receiving_po = serializers.EmailField(required=False, allow_blank=True, allow_null=True)
#     email_id_for_quote = serializers.EmailField(required=False, allow_blank=True, allow_null=True)
#     is_delete = serializers.BooleanField(required=False, allow_null=True)
#     order_by = serializers.CharField(required=False, allow_blank=True, allow_null=True, write_only=True)
#     order_type = serializers.CharField(required=False, allow_blank=True, allow_null=True, write_only=True)
#     page = serializers.IntegerField(required=False, write_only=True, allow_null=True)
#     page_size = serializers.IntegerField(required=False, write_only=True, allow_null=True)
#
#     class Meta:
#         model = SupplierContactDetails
#         fields = ('contact_person', 'main_phone_number', 'main_email_id', 'finance_phone_number',
#                   'finance_email_id', 'remittance_email_id', 'email_for_receiving_po',
#                   'email_id_for_quote', 'is_delete', 'order_by', 'order_type', 'page', 'page_size')
#
#
# class SupplierContactDetailsReadSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = SupplierContactDetails
#         fields = ('id', 'contact_person', 'main_phone_number', 'main_email_id', 'finance_phone_number',
#                   'finance_email_id', 'remittance_email_id', 'email_for_receiving_po',
#                   'email_id_for_quote', 'created_by', 'modified_by', 'created_on', 'modified_on')
#         read_only_fields = ('created_by', 'modified_by', 'created_on', 'modified_on')


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'
        read_only_fields = ('created_on', 'modified_on')


class CountryReadSerializer(serializers.ModelSerializer):
    created_by = serializers.SerializerMethodField(read_only=True)
    modified_by = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Country
        fields = (
            "id", "country_name", "country_code", "description", "created_by",
            "modified_by", "created_on", "modified_on", "is_active"
        )

    def get_created_by(self, obj):
        data = User.objects.filter(id=obj.created_by).first()
        if data:
            return f"{data.first_name} {data.last_name}".strip()
        else:
            return None

    def get_modified_by(self, obj):
        data = User.objects.filter(id=obj.modified_by).first()
        if data:
            return f"{data.first_name} {data.last_name}".strip()
        else:
            return None


class CountryFilterSerializer(serializers.Serializer):
    country_name = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    country_code = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    description = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    created_on = serializers.DateTimeField(allow_null=True, required=False)
    created_by = serializers.IntegerField(allow_null=True, required=False)
    modified_on = serializers.DateTimeField(allow_null=True, required=False)
    modified_by = serializers.IntegerField(allow_null=True, required=False)
    is_active = serializers.BooleanField(allow_null=True, required=False)
    order_by = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    order_type = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    export = serializers.BooleanField(required=False, allow_null=True, default=False)
    page = serializers.IntegerField(required=False, allow_null=True)
    page_size = serializers.IntegerField(required=False, allow_null=True)


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = '__all__'
        read_only_fields = ('created_on', 'modified_on',)


class CurrencyReadSerializer(serializers.ModelSerializer):
    created_by = serializers.SerializerMethodField(read_only=True)
    modified_by = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Currency
        fields = (
            "id", "currency_name", "currency_code", "created_by",
            "modified_by", "created_on", "modified_on", "is_active"
        )

    def get_created_by(self, obj):
        data = User.objects.filter(id=obj.created_by).first()
        if data:
            return f"{data.first_name} {data.last_name}".strip()
        else:
            return None

    def get_modified_by(self, obj):
        data = User.objects.filter(id=obj.modified_by).first()
        if data:
            return f"{data.first_name} {data.last_name}".strip()
        else:
            return None


class CurrencyFilterSerializer(serializers.Serializer):
    currency_name = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    currency_code = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    # country_code = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    created_on = serializers.DateTimeField(allow_null=True, required=False)
    created_by = serializers.IntegerField(allow_null=True, required=False)
    modified_on = serializers.DateTimeField(allow_null=True, required=False)
    modified_by = serializers.IntegerField(allow_null=True, required=False)
    is_active = serializers.BooleanField(allow_null=True, required=False)
    order_by = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    order_type = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    export = serializers.BooleanField(required=False, allow_null=True, default=False)
    page = serializers.IntegerField(required=False, allow_null=True)
    page_size = serializers.IntegerField(required=False, allow_null=True)


class CategorySerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(source='created_by.first_name', required=False, read_only=True)
    modified_by = serializers.CharField(source='modified_by.first_name', required=False, read_only=True)

    class Meta:
        model = Category
        fields = ("id", "name", "modified_on", "modified_by", "created_on",
                  "created_by")
        read_only_fields = ('created_by', 'modified_by', 'created_on', 'modified_on', 'deleted_at')


class CategoryFilterSerializer(serializers.ModelSerializer):
    """
    This serializer is used for category filter
    """
    name = serializers.CharField(max_length=100, required=False, allow_blank=True, allow_null=True)
    order_by = serializers.CharField(required=False, allow_blank=True, allow_null=True, write_only=True)
    order_type = serializers.CharField(required=False, allow_blank=True, allow_null=True, write_only=True)
    page = serializers.IntegerField(required=False, write_only=True, allow_null=True)
    page_size = serializers.IntegerField(required=False, write_only=True, allow_null=True)

    # export = serializers.BooleanField(required=False, allow_null=True, default=False)

    class Meta:
        model = Category
        fields = ('id', 'name', 'order_by', 'order_type', 'page', 'page_size')


class DepartmentSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(source='created_by.first_name', required=False, read_only=True)
    modified_by = serializers.CharField(source='modified_by.first_name', required=False, read_only=True)

    class Meta:
        model = Department
        fields = "__all__"
        read_only_fields = ('created_by', 'modified_by', 'is_delete', 'modified_on', 'deleted_at')

    def create(self, validated_data):
        try:
            name = validated_data.get('department_name').lower()

            if Department.objects.filter(department_name__iexact=name).exists():
                raise serializers.ValidationError("Department name should be unique")
            instance = super(DepartmentSerializer, self).create(validated_data)
            return instance
        except serializers.ValidationError as ve:
            raise serializers.ValidationError(ve.detail)
        except Exception as ee:
            raise serializers.ValidationError(str(ee))

    def update(self, instance, validated_data):
        try:
            # Check if department_name is provided
            name = validated_data.get('department_name')

            if name:
                name = name.lower()
                if Department.objects.filter(department_name__iexact=name).exclude(id=instance.id).exists():
                    raise serializers.ValidationError("Department name should be unique")

            # Proceed with the update
            instance = super(DepartmentSerializer, self).update(instance, validated_data)
            return instance
        except serializers.ValidationError as ve:
            raise serializers.ValidationError(ve.detail)
        except Exception as ee:
            raise serializers.ValidationError(str(ee))


class DepartmentReadSerializer(serializers.ModelSerializer):
    # id = serializers.SerializerMethodField(source='id')
    # department_type = CategorySerializer('department_type')
    created_by = serializers.CharField(source='created_by.first_name')
    # modified_by=serializers.CharField(source='modified_by.first_name')
    modified_by = serializers.SerializerMethodField(source='get_modified_by')

    class Meta:
        model = Department
        fields = (
            'id', 'department_name', 'department_code', 'is_active', 'created_by', 'modified_by', 'created_on',
            'modified_on')
        read_only_fields = ('modified_on', 'is_delete')

    def get_modified_by(self, obj):
        if obj.modified_by:
            return obj.modified_by.first_name
        return None  # or return a default value like 'Unknown'


class DepartmentFilterSerializer(serializers.ModelSerializer):
    """
    This serializer is used for department filter
    """
    name = serializers.CharField(source='department_name', required=False, allow_blank=True, allow_null=True)
    order_by = serializers.CharField(required=False, allow_blank=True, allow_null=True, write_only=True)
    order_type = serializers.CharField(required=False, allow_blank=True, allow_null=True, write_only=True)
    page = serializers.IntegerField(required=False, write_only=True, allow_null=True)
    page_size = serializers.IntegerField(required=False, write_only=True, allow_null=True)

    # export = serializers.BooleanField(required=False, allow_null=True, default=False)

    class Meta:
        model = Department
        fields = ('name', 'order_by', 'order_type', 'page', 'page_size', "is_active")
        # read_only_fields = ('department_code','department_name')


class UserDepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDepartment
        fields = "__all__"
        read_only_fields = ('created_by', 'modified_by', 'is_delete')


class StatusSerializer(serializers.ModelSerializer):
    """
    This serializer is used to create and update the status.
    """

    created_by = serializers.SerializerMethodField(source='get_created_by')
    modified_by = serializers.SerializerMethodField(source='get_modified_by')

    class Meta:
        model = Status
        fields = '__all__'
        read_only_fields = ('created_by', 'modified_by', 'created_on', 'modified_on', 'deleted_at')

    def get_created_by(self, obj):
        return obj.created_by.first_name if obj.created_by else None

    def get_modified_by(self, obj):
        return obj.modified_by.first_name if obj.modified_by else None


class StatusFilterSerializer(serializers.ModelSerializer):
    """
    This serializer is used for status filter
    """
    # name = serializers.CharField(max_length=100, required=False, allow_blank=True, allow_null=True)
    order_by = serializers.CharField(required=False, allow_blank=True, allow_null=True, write_only=True)
    order_type = serializers.CharField(required=False, allow_blank=True, allow_null=True, write_only=True)
    page = serializers.IntegerField(required=False, write_only=True, allow_null=True)
    page_size = serializers.IntegerField(required=False, write_only=True, allow_null=True)
    created_by = serializers.SerializerMethodField(source='get_created_by', required=False)
    modified_by = serializers.SerializerMethodField(source='get_modified_by', required=False)

    # created_by = serializers.SerializerMethodField(required=False,)

    # export = serializers.BooleanField(required=False, allow_null=True, default=False)

    class Meta:
        model = Status
        fields = '__all__'
        read_only_fields = ('created_by', 'modified_by', 'created_on', 'modified_on', 'deleted_at')

    def get_created_by(self, obj):
        return obj.created_by.first_name if obj.created_by else None

    def get_modified_by(self, obj):
        return obj.modified_by.first_name if obj.modified_by else None


class StatusReadSerializer(serializers.ModelSerializer):
    """
    This serializer is used for response data of Status
    """
    created_by = serializers.SerializerMethodField(source='get_created_by', read_only=True)
    modified_by = serializers.SerializerMethodField(source='get_modified_by', read_only=True)

    class Meta:
        model = Status
        fields = (
            "id", "name", "status_code", "color_code", "highlight", "modified_on", "modified_by",
            "created_on", "created_by")

    def get_modified_by(self, obj):
        data = User.objects.filter(id=obj.modified_by).first()
        if data:
            return f"{data.first_name} {data.last_name}".strip()
        else:
            return None

    def get_created_by(self, obj):
        data = User.objects.filter(id=obj.created_by).first()
        if data:
            return f"{data.first_name} {data.last_name}".strip()
        else:
            return None


class EmailTemplateTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailTemplateType
        fields = '__all__'
        read_only_fields = ['created_by', 'created_on', 'modified_by', 'modified_on']


class EmailTemplateSerializer(serializers.ModelSerializer):
    SHORTCODES = [
        '##register_user_email##', '##user_email##', '##user_name##', '##creator_email##',
        '##behalf_email##', '##follower_email##', '##queue_manager_email##', '##assigned_to_email##',
        '##ticket_no##', '##user_password##', '##otp_password##', '##requester_name##',
        '##queue_manager_name##', '##assigned_to_name##', '##action_by_name##', '##new_password##'
    ]

    class Meta:
        model = EmailTemplate
        fields = '__all__'
        read_only_fields = ['created_by', 'created_on', 'modified_on', 'modified_by']

    def validate_field_for_shortcodes(self, field_value, field_name):
        if field_value:
            if not any(shortcode in field_value for shortcode in self.SHORTCODES):
                raise serializers.ValidationError(f"The {field_name} field must contain at least one valid shortcode.")
        return field_value

    def validate_email_to(self, value):
        return self.validate_field_for_shortcodes(value, "email_to")

    def validate_cc(self, value):
        if value:
            emails = [email.strip() for email in value.split(',')]
            return ','.join([self.validate_field_for_shortcodes(email, "cc") for email in emails])
        return value

    def validate_bcc(self, value):
        if value:
            emails = [email.strip() for email in value.split(',')]
            return ','.join([self.validate_field_for_shortcodes(email, "bcc") for email in emails])
        return value

    def validate_message(self, value):
        return self.validate_field_for_shortcodes(value, "message")

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['cc'] = instance.cc.split(',') if instance.cc else []
        representation['bcc'] = instance.bcc.split(',') if instance.bcc else []
        return representation

    def to_internal_value(self, data):
        # Ensure that cc and bcc are handled properly if they are in the data
        cc = data.get('cc')
        bcc = data.get('bcc')

        if cc is not None:
            data['cc'] = ','.join(cc) if isinstance(cc, list) else cc

        if bcc is not None:
            data['bcc'] = ','.join(bcc) if isinstance(bcc, list) else bcc

        return super().to_internal_value(data)


class EmailTemplateFilterSerializer(serializers.ModelSerializer):
    """
    This serializer is used for email template filter.
    """
    template_type = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    subject = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    order_by = serializers.CharField(required=False, allow_blank=True, allow_null=True, write_only=True)
    order_type = serializers.CharField(required=False, allow_blank=True, allow_null=True, write_only=True)
    page = serializers.IntegerField(required=False, write_only=True, allow_null=True)
    page_size = serializers.IntegerField(required=False, write_only=True, allow_null=True)

    class Meta:
        model = EmailTemplate
        fields = ('template_type', 'subject', 'order_by', 'order_type', 'page', 'page_size', "is_active")


class EmailTemplateReadSerializer(serializers.ModelSerializer):
    """
    This serializer is used to read email template data.
    """
    created_by = serializers.CharField(source='created_by.first_name', read_only=True)
    modified_by = serializers.SerializerMethodField()
    template_type = serializers.CharField(source='template_type.template_name', read_only=True)

    class Meta:
        model = EmailTemplate
        fields = (
            'id', 'template_type', 'subject', 'email_to', 'cc', 'bcc', 'message', 'signature',
            'is_active', 'created_by', 'modified_by', 'created_on', 'modified_on'
        )
        read_only_fields = ('created_on', 'modified_on')

    def get_modified_by(self, obj):
        if obj.modified_by:
            return obj.modified_by.first_name
        return None

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['cc'] = instance.cc.split(',') if instance.cc else []
        representation['bcc'] = instance.bcc.split(',') if instance.bcc else []
        return representation


class UserStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserStatus
        fields = '__all__'
        # Only 'created_by' and 'created_on' should be read-only
        read_only_fields = ('created_by', 'created_on')

    def validate(self, attrs):
        """
        Override the validate method to ensure the unique constraint on 'user_id' and 'status_id' is respected.
        """
        user_id = attrs.get('user_id')
        status_id = attrs.get('status_id')
        instance = self.instance

        # Check if another record with the same user_id and status_id exists, excluding the current instance
        if UserStatus.objects.filter(user_id=user_id, status_id=status_id).exclude(
                id=instance.id if instance else None).exists():
            raise serializers.ValidationError("A record with this user_id and status_id already exists.")

        return attrs

    def update(self, instance, validated_data):
        """
        Override the update method to handle 'modified_by' and 'modified_on' fields manually.
        """
        # Update the instance with the validated data
        instance.status_id = validated_data.get('status_id', instance.status_id)
        instance.is_active = validated_data.get('is_active', instance.is_active)

        # The 'modified_by' and 'modified_on' fields will be set in the view
        instance.save()
        return instance


class StatusFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatusField
        fields = '__all__'
        read_only_fields = ('created_by', 'created_on', 'modified_by', 'modified_on')

    def validate(self, data):
        status_code = data.get('status_code')
        field_name = data.get('field_name')
        if StatusField.objects.filter(status_code=status_code, field_name=field_name).exists():
            raise serializers.ValidationError("The combination of status_code and field_name must be unique.")
        return data


# class SupplierContactDetailsSerializer2(serializers.ModelSerializer):
#     class Meta:
#         model = SupplierContactDetails
#         fields = '__all__'
#
#     def validate(self, data):
#         request_user = self.context['request'].user.id
#         # This will fetch the latest Status code of the user. Based on this will check and throw error.
#         user_status = UserStatus.objects.filter(user=request_user).order_by('-created_on').first()
#
#         # Check if user status code is 5
#         print(user_status.status)
#         if int(user_status.status) != 9:
#             raise serializers.ValidationError(
#                 "Supplier contact details can only be created if the user's status code is 9."
#             )
#
#         # Check if the status allows creating the requested fields
#         status_fields = StatusField.objects.filter(status_code=user_status.status)
#         allowed_fields = set(status_fields.values_list('field_name', flat=True))
#
#         for field in data.keys():
#             if field not in allowed_fields:
#                 raise serializers.ValidationError(
#                     f"Field '{field}' is not allowed to create or update for the current user status."
#                 )
#
#         return data
#
#     def create(self, validated_data):
#         validated_data['created_by'] = self.context['request'].user.id
#         return super().create(validated_data)


class UserStatusFieldSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    status_codes = serializers.ListField(child=serializers.IntegerField())
    status_fields = serializers.ListField(child=serializers.ListField(
        child=serializers.CharField()
    ))


class ActivityLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityLog
        # fields = ['id', 'module_name', 'action_type', 'action_date', 'username', 'data_changes']
        # read_only_fields = ['id', 'action_date']
        fields = '__all__'


class ActivityLogReadSerializer(serializers.ModelSerializer):
    """
    Serializer for reading ActivityLog data.
    """
    created_by = serializers.SerializerMethodField(source='get_created_by', read_only=True)
    modified_by = serializers.SerializerMethodField(source='get_modified_by', read_only=True)
    user_email_id = serializers.SerializerMethodField(source='get_user_email_id', read_only=True)

    # user_email_id = serializers.SerializerMethodField(source='get_user_email_id', read_only=True)

    class Meta:
        model = ActivityLog
        fields = '__all__'

    def get_created_by(self, obj):
        data = User.objects.filter(id=obj.created_by_id).first()
        return f"{data.first_name} {data.last_name}".strip() if data else None

    def get_modified_by(self, obj):
        data = User.objects.filter(id=obj.modified_by_id).first()
        return f"{data.first_name} {data.last_name}".strip() if data else None

    def get_user_email_id(self, obj):
        # Assuming action_by refers to an ID or email field in User model
        if obj.action_by:
            # Check what field action_by should match in User model, such as email
            user = User.objects.filter(email=obj.action_by).first()  # Adjust this line if needed
            return user.email if user else None
        return None


class ActivityLogFilterSerializer(serializers.ModelSerializer):
    """
    Serializer for filtering ActivityLog records.
    """
    module_id = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    column_name = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    before_input = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    after_input = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    action_type = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    action_by = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    action_date = serializers.DateTimeField(required=False, allow_null=True)
    table_name = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    ip_address = serializers.IPAddressField(required=False, allow_blank=True, allow_null=True)
    remote_url = serializers.URLField(required=False, allow_blank=True, allow_null=True)
    user_agent = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    created_by = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False, allow_null=True)
    modified_by = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False, allow_null=True)
    created_on = serializers.DateTimeField(required=False, allow_null=True)
    modified_on = serializers.DateTimeField(required=False, allow_null=True)
    deleted_at = serializers.DateTimeField(required=False, allow_null=True)
    order_by = serializers.CharField(required=False, allow_blank=True, allow_null=True, write_only=True)
    order_type = serializers.CharField(required=False, allow_blank=True, allow_null=True, write_only=True)
    page = serializers.IntegerField(required=False, write_only=True, allow_null=True)
    page_size = serializers.IntegerField(required=False, write_only=True, allow_null=True)
    user_email_id = serializers.EmailField(required=False, write_only=True, allow_null=True)
    export = serializers.BooleanField(required=False, allow_null=True, default=False)

    class Meta:
        model = ActivityLog
        fields = (
            'module_id', 'column_name', 'before_input', 'after_input', 'action_type', 'action_by', 'action_date',
            'table_name', 'ip_address', 'remote_url', 'user_agent', 'created_by', 'modified_by', 'export',
            'created_on', 'modified_on', 'deleted_at', 'order_by', 'order_type', 'page', 'page_size', 'user_email_id'
        )
        read_only_fields = ('created_on', 'modified_on', 'deleted_at')


class ModuleEnumSerializer(serializers.Serializer):
    module_id = serializers.IntegerField()
    module_name = serializers.CharField(max_length=255)


class LineOfBusinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = LineOfBusiness
        fields = ['id', 'name', 'description', 'created_by', 'modified_by', 'created_on', 'modified_on', 'is_active',
                  'is_delete']
        read_only_fields = ('created_by', 'modified_by', 'created_on', 'modified_on', 'is_delete')

    def create(self, validated_data):
        return LineOfBusiness.objects.create(**validated_data)


class LineOfBusinessUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = LineOfBusiness
        fields = '__all__'
        read_only_fields = ('created_by', 'modified_by', 'created_on', 'modified_on', 'is_delete')


class LineOfBusinessFilterSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    is_active = serializers.BooleanField(required=False, allow_null=True)
    is_delete = serializers.BooleanField(required=False, allow_null=True)
    page = serializers.IntegerField(required=False, write_only=True, allow_null=True)
    page_size = serializers.IntegerField(required=False, write_only=True, allow_null=True)
    order_by = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    order_type = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    class Meta:
        model = LineOfBusiness
        fields = ('name', 'is_active', 'is_delete', 'page', 'page_size', 'order_by', 'order_type')


class LineOfBusinessReadSerializer(serializers.ModelSerializer):
    created_by = serializers.SerializerMethodField(source='get_created_by', read_only=True)
    modified_by = serializers.SerializerMethodField(source='get_modified_by', read_only=True)

    def get_created_by(self, obj):
        user = CustomUser.objects.filter(id=obj.created_by).first()
        return '{} {}'.format(user.first_name, user.last_name).strip() if user else None

    def get_modified_by(self, obj):
        user = CustomUser.objects.filter(id=obj.modified_by).first()
        return '{} {}'.format(user.first_name, user.last_name).strip() if user else None

    class Meta:
        model = LineOfBusiness
        fields = "__all__"
        read_only_fields = ('created_on', 'modified_on', 'is_delete')


class LegalEntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = LegalEntity
        fields = '__all__'
        read_only_fields = ('created_on', 'modified_on')

    def create(self, validated_data):
        return LegalEntity.objects.create(**validated_data)

    def update(self, instance, validated_data):
        # Only update fields present in validated_data
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class LegalEntityReadSerializer(serializers.ModelSerializer):
    created_by = serializers.SerializerMethodField(source='get_created_by', read_only=True)
    modified_by = serializers.SerializerMethodField(source='get_modified_by', read_only=True)

    # country = serializers.SerializerMethodField(source='get_country', read_only=True)

    # destination_hold = serializers.SerializerMethodField(read_only=True, source='get_destination_hold')
    # review_flag = serializers.SerializerMethodField(read_only=True, source='get_review_flag')

    class Meta:
        model = LegalEntity
        fields = (
            'legal_entity_id', 'legal_entity_name', 'address_city', 'address_country_region_id',
            'address_country_region_iso_code', 'address_description', 'address_street', 'address_zip_code',
            'vendor_account_number', 'sales_tax_group_code', 'bank_account_id', 'currency_code',
            'on_hold_status', 'vendor_group_id', 'vendor_hold_release_date', 'vendor_organization_name',
            'vendor_type', 'vend_source_system', 'vend_source_system_id', 'vat_number', 'created_by',
            'modified_by', 'created_on', 'modified_on'
        )

    def get_created_by(self, obj):
        user = CustomUser.objects.filter(id=obj.created_by).first()
        return '{} {}'.format(user.first_name, user.last_name).strip() if user else None

    def get_modified_by(self, obj):
        user = CustomUser.objects.filter(id=obj.modified_by).first()
        return '{} {}'.format(user.first_name, user.last_name).strip() if user else None

    # def get_destination_hold(self, obj):
    #     return LineOfBusinessSerializer(obj.destination_hold.all(), many=True).data
    #
    # def get_review_flag(self, obj):
    #     return LineOfBusinessSerializer(obj.review_flag.all(), many=True).data
    def get_country(self, obj):
        try:
            country = Country.objects.get(id=obj.country_id)
            return CountrySerializer(country).data["country_code"]
        except Country.DoesNotExist:
            return None


class LegalEntityFilterSerializer(serializers.Serializer):
    legal_entity_id = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    legal_entity_name = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    address_city = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    address_country_region_id = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    address_country_region_iso_code = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    address_description = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    address_street = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    address_zip_code = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    vendor_account_number = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    sales_tax_group_code = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    bank_account_id = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    currency_code = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    on_hold_status = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    vendor_group_id = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    vendor_hold_release_date = serializers.DateField(allow_null=True, required=False)
    vendor_organization_name = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    vendor_type = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    vend_source_system = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    vend_source_system_id = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    vat_number = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    order_by = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    order_type = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    page = serializers.IntegerField(required=False, allow_null=True)
    page_size = serializers.IntegerField(required=False, allow_null=True)
    export = serializers.BooleanField(required=False, allow_null=True, default=False)


# class DestinationReviewSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = DestinationReview
#         fields = '__all__'
#         read_only_fields = ('created_on', 'modified_on',)
#
#
# class DestinationReviewReadSerializer(serializers.ModelSerializer):
#     created_by = serializers.SerializerMethodField(read_only=True)
#     modified_by = serializers.SerializerMethodField(read_only=True)
#
#     class Meta:
#         model = DestinationReview
#         fields = (
#             'id', 'name', 'description', 'type', 'created_by', 'modified_by',
#             'created_on', 'modified_on', 'is_active', 'is_delete'
#         )
#
#     def get_created_by(self, obj):
#         user = CustomUser.objects.filter(id=obj.created_by).first()
#         return f"{user.first_name} {user.last_name}".strip() if user else None
#
#     def get_modified_by(self, obj):
#         user = CustomUser.objects.filter(id=obj.modified_by).first()
#         return f"{user.first_name} {user.last_name}".strip() if user else None

class VendorFilterSerializer(serializers.ModelSerializer):
    vat_number = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    supplier_type = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    dfds_entity_code = serializers.IntegerField(required=False, allow_null=True)
    currency = serializers.IntegerField(required=False, allow_null=True)
    supplier_source_system = serializers.IntegerField(required=False, allow_null=True)
    order_by = serializers.CharField(required=False, allow_blank=True, allow_null=True, write_only=True)
    order_type = serializers.CharField(required=False, allow_blank=True, allow_null=True, write_only=True)
    page = serializers.IntegerField(required=False, write_only=True, allow_null=True)
    page_size = serializers.IntegerField(required=False, write_only=True, allow_null=True)

    class Meta:
        model = Vendor
        fields = (
            'vat_number', 'supplier_type', 'dfds_entity_code', 'currency', 'supplier_source_system',
            'order_by', 'order_type', 'page', 'page_size'
        )


class VendorReadSerializer(serializers.ModelSerializer):
    currency = serializers.SerializerMethodField()
    supplier_source_system = serializers.SerializerMethodField()
    dfds_entity_code = serializers.SerializerMethodField()
    created_by = serializers.SerializerMethodField()
    modified_by = serializers.SerializerMethodField()

    class Meta:
        model = Vendor
        fields = (
            'id', 'vat_number', 'dfds_entity_code', 'currency', 'supplier_source_system', 'supplier_type', 'created_by',
            'created_on', 'modified_by', 'modified_on',)

    def get_currency(self, obj):
        """
        Returns the name of the Currency associated with the vendor based on the currency ID.
        """
        if obj.currency:
            try:
                currency = Currency.objects.get(id=obj.currency)
                return currency.currency_name
            except Currency.DoesNotExist:
                return None
        return None

    def get_supplier_source_system(self, obj):
        """
        Returns the name of the LineOfBusiness associated with the vendor based on the supplier_source_system ID.
        """
        if obj.supplier_source_system:
            try:
                line_of_business = LineOfBusiness.objects.get(id=obj.supplier_source_system)
                return line_of_business.name
            except LineOfBusiness.DoesNotExist:
                return None
        return None

    #
    def get_dfds_entity_code(self, obj):
        """
        Returns the name of the LegalEntity associated with the vendor based on the dfds_entity_code ID.
        """
        if obj.dfds_entity_code:
            try:
                legal_entity = LegalEntity.objects.get(id=obj.dfds_entity_code)
                return legal_entity.legal_entity_name
            except LegalEntity.DoesNotExist:
                return None
        return None

    def get_created_by(self, obj):
        if obj.created_by:
            try:
                user = CustomUser.objects.get(id=obj.created_by)
                return f"{user.first_name} {user.last_name}".strip()
            except CustomUser.DoesNotExist:
                return None

    def get_modified_by(self, obj):
        if obj.modified_by:
            try:
                user = CustomUser.objects.get(id=obj.modified_by)
                return f"{user.first_name} {user.last_name}".strip()
            except CustomUser.DoesNotExist:
                return None


class VendorCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ('vat_number', 'dfds_entity_code', 'currency', 'supplier_source_system', 'supplier_type')

    def validate_supplier_source_system(self, value):
        if not LineOfBusiness.objects.filter(id=value).exists():
            raise serializers.ValidationError("Invalid supplier source system ID")
        return value

    def validate_currency(self, value):
        if not Currency.objects.filter(id=value).exists():
            raise serializers.ValidationError("Invalid currency ID")
        return value

    def validate_dfds_entity_code(self, value):
        if not LegalEntity.objects.filter(id=value).exists():
            raise serializers.ValidationError("Invalid DFDS entity code ID")
        return value
