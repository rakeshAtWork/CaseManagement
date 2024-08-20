from datetime import timezone

from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from rest_framework import serializers

from .models import FileType, Client, BusinessUnit, Vendor, Application, Customer, AccountType, SupplierContactDetails, \
    D365FOSetup, CompanyInfoForValidation, CPPSanctionAssessment, VendorDetails, Currency, Country, Category, \
    Department, UserDepartment, Status, EmailTemplate

User = get_user_model()


class FileTypeSerializers(serializers.ModelSerializer):
    class Meta:
        model = FileType
        fields = (
            "id", "status", "file_type", "file_extension", "max_file_size", "file_description", "created_by",
            "updated_by", "created_on", "updated_on",)
        read_only_fields = ("created_by", "updated_by", "created_on", "updated_on")

    def create(self, validated_data):
        try:
            file_extension = validated_data.get('file_extension').lower()

            regex_validator = RegexValidator(
                regex=r'^[a-zA-Z0-9]+$',
                message="File extension should not contain any special characters"
            )
            regex_validator(file_extension)

            if FileType.objects.filter(file_extension__iexact=file_extension).exists():
                raise serializers.ValidationError("File extension name should be unique")
            instance = super(FileTypeSerializers, self).create(validated_data)
            return instance
        except serializers.ValidationError as ve:
            raise serializers.ValidationError(ve.detail)
        except Exception as ee:
            raise serializers.ValidationError(str(ee))


class FileTypeReadSerializers(serializers.ModelSerializer):
    created_by = serializers.SerializerMethodField(source='get_created_by', read_only=True)
    updated_by = serializers.SerializerMethodField(source='get_updated_by', read_only=True)

    class Meta:
        model = FileType
        fields = (
            "id", "status", "file_type", "file_extension", "max_file_size", "file_description", "created_by",
            "updated_by", "created_on", "updated_on", "is_delete")

    def get_updated_by(self, obj):
        data = User.objects.filter(id=obj.updated_by).first()
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


class FileTypeFilterSerializers(serializers.Serializer):
    status = serializers.BooleanField(allow_null=True, required=False)
    file_type = serializers.CharField(allow_null=True, required=False)
    file_extension = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    max_file_size = serializers.IntegerField(allow_null=True, required=False)
    file_description = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    created_on = serializers.DateTimeField(allow_null=True, required=False)
    created_by = serializers.IntegerField(allow_null=True, required=False)
    updated_on = serializers.DateTimeField(allow_null=True, required=False)
    updated_by = serializers.IntegerField(allow_null=True, required=False)
    order_by = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    order_type = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    export = serializers.BooleanField(required=False, allow_null=True, default=False)
    page = serializers.IntegerField(required=False, allow_null=True)
    page_size = serializers.IntegerField(required=False, allow_null=True)


class ClientSerializers(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = (
            "id", "status", "code", "name", "contact_name", "contact_email", "contact_number", "is_delete",
            "created_by", "updated_by", "created_on", "updated_on")
        read_only_fields = ("created_by", "updated_by", "created_on", "updated_on")

    def create(self, validated_data):
        try:
            name = validated_data.get('name').lower()
            code = validated_data.get('code').lower()

            if Client.objects.filter(name__iexact=name).exists():
                raise serializers.ValidationError("Client name should be unique")
            if Client.objects.filter(code__iexact=code).exists():
                raise serializers.ValidationError("Client code should be unique")
            instance = super(ClientSerializers, self).create(validated_data)
            return instance
        except serializers.ValidationError as ve:
            raise serializers.ValidationError(ve.detail)
        except Exception as ee:
            raise serializers.ValidationError(str(ee))


class ClientReadSerializers(serializers.ModelSerializer):
    # created_by = serializers.SerializerMethodField(source='get_created_by', read_only=True)
    # updated_by = serializers.SerializerMethodField(source='get_updated_by', read_only=True)

    class Meta:
        model = Client
        fields = (
            "id", "status", "code", "name", "contact_name", "contact_email", "contact_number", "is_delete",
            "created_by", "updated_by", "created_on", "updated_on")

    # def get_updated_by(self, obj):
    #     data = User.objects.filter(id=obj.updated_by).first()
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


class ClientFilterSerializers(serializers.Serializer):
    status = serializers.BooleanField(allow_null=True, required=False)
    code = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    name = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    contact_name = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    contact_email = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    contact_number = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    is_delete = serializers.BooleanField(allow_null=True, required=False)
    created_on = serializers.DateTimeField(allow_null=True, required=False)
    created_by = serializers.IntegerField(allow_null=True, required=False)
    updated_on = serializers.DateTimeField(allow_null=True, required=False)
    updated_by = serializers.IntegerField(allow_null=True, required=False)
    order_by = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    order_type = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    export = serializers.BooleanField(required=False, allow_null=True, default=False)
    page = serializers.IntegerField(required=False, allow_null=True)
    page_size = serializers.IntegerField(required=False, allow_null=True)


class CustomerSerializers(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = (
            "id",
            "client_id", "status", "code", "name", "contact_name", "contact_email", "contact_number", "is_delete",
            "retention_period", "disposal_action", "disposal_notification_period",
            "created_by", "updated_by", "created_on", "updated_on")
        read_only_fields = ("created_by", "updated_by", "created_on", "updated_on")

    def create(self, validated_data):
        try:
            name = validated_data.get('name').lower()
            code = validated_data.get('code').lower()

            if Customer.objects.filter(name__iexact=name).exists():
                raise serializers.ValidationError("Customer name should be unique")
            if Customer.objects.filter(code__iexact=code).exists():
                raise serializers.ValidationError("Customer code should be unique")
            instance = super(CustomerSerializers, self).create(validated_data)
            return instance

        except Exception as ee:
            raise serializers.ValidationError(str(ee))


class CustomerReadSerializers(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = (
            "id", "client_id", "status", "code", "name", "contact_name", "contact_email", "contact_number", "is_delete",
            "retention_period", "disposal_action", "disposal_notification_period",
            "created_by", "updated_by", "created_on", "updated_on")


class CustomerFilterSerializers(serializers.Serializer):
    status = serializers.BooleanField(allow_null=True, required=False)
    client_id = serializers.CharField(allow_null=True, required=False)
    code = serializers.CharField(allow_null=True, required=False)
    name = serializers.CharField(allow_null=True, required=False)
    contact_name = serializers.CharField(allow_null=True, required=False)
    contact_email = serializers.CharField(allow_null=True, required=False)
    contact_number = serializers.CharField(allow_null=True, required=False)
    retention_period = serializers.IntegerField(allow_null=True, required=False)
    disposal_action = serializers.CharField(allow_null=True, required=False)
    disposal_notification_period = serializers.IntegerField(allow_null=True, required=False)
    is_delete = serializers.BooleanField(allow_null=True, required=False)
    created_on = serializers.DateTimeField(allow_null=True, required=False)
    created_by = serializers.IntegerField(allow_null=True, required=False)
    updated_on = serializers.DateTimeField(allow_null=True, required=False)
    updated_by = serializers.IntegerField(allow_null=True, required=False)
    order_by = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    order_type = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    export = serializers.BooleanField(required=False, allow_null=True, default=False)
    page = serializers.IntegerField(required=False, allow_null=True)
    page_size = serializers.IntegerField(required=False, allow_null=True)


class BusinessUnitSerializers(serializers.ModelSerializer):
    class Meta:
        model = BusinessUnit
        fields = (
            "id", "client_id", "code", "name", "contact_name", "contact_email", "contact_number",
            "created_by", "updated_by", "created_on", "updated_on", "is_delete", "status")
        read_only_fields = ("created_by", "updated_by", "created_on", "updated_on")

    def create(self, validated_data):
        try:
            name = validated_data.get('name').lower()
            code = validated_data.get('code').lower()

            if BusinessUnit.objects.filter(name__iexact=name).exists():
                raise serializers.ValidationError("Business Unit name should be unique")
            if BusinessUnit.objects.filter(code__iexact=code).exists():
                raise serializers.ValidationError("Business Unit code should be unique")
            instance = super(BusinessUnitSerializers, self).create(validated_data)
            return instance
        except serializers.ValidationError as ve:
            raise serializers.ValidationError(ve.detail)
        except Exception as ee:
            raise serializers.ValidationError(str(ee))


class BusinessUnitReadSerializers(serializers.ModelSerializer):
    class Meta:
        model = BusinessUnit
        fields = (
            "id", "client_id", "code", "name", "contact_name", "contact_email", "contact_number",
            "created_by", "updated_by", "created_on", "updated_on", "is_delete", "status")

    def get_updated_by(self, obj):
        data = User.objects.filter(id=obj.updated_by).first()
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


class BusinessUnitFilterSerializers(serializers.Serializer):
    status = serializers.BooleanField(required=False, allow_null=True)
    client_id = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    is_delete = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    code = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    name = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    contact_name = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    contact_email = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    contact_number = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    created_on = serializers.DateTimeField(allow_null=True, required=False)
    created_by = serializers.IntegerField(allow_null=True, required=False)
    updated_on = serializers.DateTimeField(allow_null=True, required=False)
    updated_by = serializers.IntegerField(allow_null=True, required=False)
    order_by = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    order_type = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    page = serializers.IntegerField(required=False, allow_null=True)
    page_size = serializers.IntegerField(required=False, allow_null=True)
    export = serializers.BooleanField(required=False, allow_null=True, default=False)


class VendorSerializers(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = (
            "id", "is_delete", "customer_id", "status", "code", "name", "contact_name", "contact_email",
            "contact_number", "retention_period", "disposal_action", "disposal_notification_period",
            "created_by", "updated_by", "created_on", "updated_on")
        read_only_fields = ("created_by", "updated_by", "created_on", "updated_on")

    def create(self, validated_data):
        try:
            name = validated_data.get('name').lower()
            code = validated_data.get('code').lower()

            if Vendor.objects.filter(name__iexact=name).exists():
                raise serializers.ValidationError("Vendor name should be unique")
            if Vendor.objects.filter(code__iexact=code).exists():
                raise serializers.ValidationError("Vendor code should be unique")
            instance = super(VendorSerializers, self).create(validated_data)
            return instance

        except Exception as ee:
            raise serializers.ValidationError(str(ee))


class VendorReadSerializers(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = (
            "id", "is_delete", "customer_id", "status", "code", "name", "contact_name", "contact_email",
            "retention_period", "disposal_action", "disposal_notification_period",
            "contact_number", "created_by", "updated_by", "created_on", "updated_on")


class VendorFilterSerializers(serializers.Serializer):
    customer_id = serializers.CharField(allow_null=True, required=False)
    status = serializers.BooleanField(allow_null=True, required=False)
    code = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    name = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    contact_name = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    contact_email = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    contact_number = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    retention_period = serializers.IntegerField(allow_null=True, required=False)
    disposal_action = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    disposal_notification_period = serializers.IntegerField(allow_null=True, required=False)
    is_delete = serializers.BooleanField(allow_null=True, required=False)
    created_on = serializers.DateTimeField(allow_null=True, required=False)
    created_by = serializers.IntegerField(allow_null=True, required=False)
    updated_on = serializers.DateTimeField(allow_null=True, required=False)
    updated_by = serializers.IntegerField(allow_null=True, required=False)
    order_by = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    order_type = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    export = serializers.BooleanField(required=False, allow_null=True, default=False)
    page = serializers.IntegerField(required=False, allow_null=True)
    page_size = serializers.IntegerField(required=False, allow_null=True)


class ApplicationSerializers(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = (
            "id", "status", "code", "name", "created_by", "updated_by", "created_on", "updated_on", "contact_name",
            "contact_email", "contact_number", "status")
        read_only_fields = ("created_by", "updated_by", "created_on", "updated_on")


class ApplicationReadSerializers(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = (
            "id", "status", "code", "name", "created_by", "updated_by", "created_on", "updated_on",
            "contact_name", "contact_email", "contact_number", "status")


class ApplicationFilterSerializers(serializers.Serializer):
    status = serializers.BooleanField(allow_null=True, required=False)
    code = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    name = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    contact_name = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    contact_email = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    contact_number = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    created_on = serializers.DateTimeField(allow_null=True, required=False)
    created_by = serializers.IntegerField(allow_null=True, required=False)
    updated_on = serializers.DateTimeField(allow_null=True, required=False)
    updated_by = serializers.IntegerField(allow_null=True, required=False)
    order_by = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    order_type = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    export = serializers.BooleanField(required=False, allow_null=True, default=False)
    page = serializers.IntegerField(required=False, allow_null=True)
    page_size = serializers.IntegerField(required=False, allow_null=True)


class AccountTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountType
        fields = ['account_type']


class SupplierContactDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupplierContactDetails
        fields = ['id', 'contact_person', 'main_phone_number', 'main_email_id', 'finance_phone_number',
                  'finance_email_id', 'remittance_email_id', 'email_for_receiving_po', 'email_id_for_quote']


class VendorDetailsFilterSerializer(serializers.Serializer):
    company_code = serializers.CharField(required=False, allow_blank=True)
    company_name = serializers.CharField(required=False, allow_blank=True)
    agent_number = serializers.CharField(required=False, allow_blank=True)
    supplier_type = serializers.CharField(required=False, allow_blank=True)
    currency = serializers.CharField(required=False, allow_blank=True)
    terms_of_payment = serializers.CharField(required=False, allow_blank=True)
    supplier_name = serializers.CharField(required=False, allow_blank=True)
    siret_number = serializers.CharField(required=False, allow_blank=True)
    vat_country_code = serializers.CharField(required=False, allow_blank=True)
    orbis_id = serializers.CharField(required=False, allow_blank=True)
    orbis_id_found = serializers.BooleanField(required=False)
    address_line = serializers.CharField(required=False, allow_blank=True)
    country = serializers.CharField(required=False, allow_blank=True)
    postal_code = serializers.CharField(required=False, allow_blank=True)
    town = serializers.CharField(required=False, allow_blank=True)
    country_code = serializers.CharField(required=False, allow_blank=True)
    swift_number = serializers.CharField(required=False, allow_blank=True)
    is_prime_revenue = serializers.BooleanField(required=False)
    created_by = serializers.IntegerField(required=False)
    updated_by = serializers.IntegerField(required=False)
    created_on = serializers.DateTimeField(required=False)
    updated_on = serializers.DateTimeField(required=False)


class D365FOSetupSerializer(serializers.ModelSerializer):
    class Meta:
        model = D365FOSetup
        fields = '__all__'  # Include all fields in the serializer
        read_only_fields = ('created_by', 'updated_by', 'created_on', 'updated_on')

    def update(self, instance, validated_data):
        # You can add custom update logic here if needed
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class CompanyInfoForValidationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyInfoForValidation
        fields = ['orbis_supplier', 'orbis_bvd', 'vat_supplier', 'vat_validity', 'vat_validity_date']


class CPPSanctionAssessmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CPPSanctionAssessment
        fields = ['cfra_score', 'cfra_portfolio_id', 'cfra_score_card', 'cfra_assessment']


class VendorDetailsSerializer(serializers.ModelSerializer):
    account_type = AccountTypeSerializer()
    supplier_contact_details = SupplierContactDetailsSerializer()
    d365fo_setup = D365FOSetupSerializer()
    company_info_for_validation = CompanyInfoForValidationSerializer()
    cpp_sanction_assessment = CPPSanctionAssessmentSerializer()

    class Meta:
        model = VendorDetails
        fields = '__all__'

    def create(self, validated_data):
        # Extract nested data
        account_type_data = validated_data.pop('account_type', None)
        supplier_contact_details_data = validated_data.pop('supplier_contact_details', None)
        d365fo_setup_data = validated_data.pop('d365fo_setup', None)
        company_info_for_validation_data = validated_data.pop('company_info_for_validation', None)
        cpp_sanction_assessment_data = validated_data.pop('cpp_sanction_assessment', None)

        # Create related instances and associate them with the VendorDetails instance
        if account_type_data:
            account_type_data = AccountType.objects.create(**account_type_data)

        if supplier_contact_details_data:
            supplier_contact_details_data = SupplierContactDetails.objects.create(**supplier_contact_details_data)

        if d365fo_setup_data:
            d365fo_setup_data = D365FOSetup.objects.create(**d365fo_setup_data)

        if company_info_for_validation_data:
            company_info_for_validation_data = CompanyInfoForValidation.objects.create(
                **company_info_for_validation_data)

        if cpp_sanction_assessment_data:
            cpp_sanction_assessment_data = CPPSanctionAssessment.objects.create(**cpp_sanction_assessment_data)

        # Create the VendorDetails instance at last
        vendor_details = VendorDetails.objects.create(d365fo_setup=d365fo_setup_data,
                                                      supplier_contact_details=supplier_contact_details_data,
                                                      account_type=account_type_data,
                                                      company_info_for_validation=company_info_for_validation_data,
                                                      cpp_sanction_assessment=cpp_sanction_assessment_data,
                                                      **validated_data)

        return vendor_details


class UpdateVendorDetailsSerializer(serializers.ModelSerializer):
    account_type = AccountTypeSerializer(required=False)
    supplier_contact_details = SupplierContactDetailsSerializer(required=False)
    d365fo_setup = D365FOSetupSerializer(required=False)
    company_info_for_validation = CompanyInfoForValidationSerializer(required=False)
    cpp_sanction_assessment = CPPSanctionAssessmentSerializer(required=False)

    class Meta:
        model = VendorDetails
        fields = '__all__'

    def update(self, instance, validated_data):
        account_type_data = validated_data.pop('account_type', None)
        supplier_contact_details_data = validated_data.pop('supplier_contact_details', None)
        d365fo_setup_data = validated_data.pop('d365fo_setup', None)
        company_info_for_validation_data = validated_data.pop('company_info_for_validation', None)
        cpp_sanction_assessment_data = validated_data.pop('cpp_sanction_assessment', None)

        # Update the main VendorDetails fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update nested fields
        if account_type_data:
            account_type_instance = instance.account


class D365FOSetupFilterSerializer(serializers.ModelSerializer):
    sales_tax_group = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    vendor_group = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    payment_method = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    business_unit = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    inter_company = serializers.BooleanField(required=False, allow_null=True)
    vendor_hold = serializers.BooleanField(required=False, allow_null=True)
    source_system = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    source_system_supplier_reference = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    d365fo_id = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    fs_ticket_number = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    allow_false_duplicates = serializers.BooleanField(required=False, allow_null=True)
    additional_comments = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    order_by = serializers.CharField(required=False, allow_blank=True, allow_null=True, write_only=True)
    order_type = serializers.CharField(required=False, allow_blank=True, allow_null=True, write_only=True)
    page = serializers.IntegerField(required=False, write_only=True, allow_null=True)
    page_size = serializers.IntegerField(required=False, write_only=True, allow_null=True)

    class Meta:
        model = D365FOSetup
        fields = ('sales_tax_group', 'vendor_group', 'payment_method', 'business_unit', 'inter_company',
                  'vendor_hold', 'source_system', 'source_system_supplier_reference', 'd365fo_id',
                  'fs_ticket_number', 'allow_false_duplicates', 'additional_comments', 'order_by',
                  'order_type', 'page', 'page_size')


class D365FOSetupReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = D365FOSetup
        fields = ('id', 'sales_tax_group', 'vendor_group', 'payment_method', 'business_unit',
                  'inter_company', 'vendor_hold', 'source_system', 'source_system_supplier_reference',
                  'd365fo_id', 'fs_ticket_number', 'allow_false_duplicates', 'additional_comments',
                  'created_by', 'updated_by', 'created_on', 'updated_on')
        read_only_fields = ('created_by', 'updated_by', 'created_on', 'updated_on')


class SupplierContactDetailsFilterSerializer(serializers.ModelSerializer):
    contact_person = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    main_phone_number = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    main_email_id = serializers.EmailField(required=False, allow_blank=True, allow_null=True)
    finance_phone_number = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    finance_email_id = serializers.EmailField(required=False, allow_blank=True, allow_null=True)
    remittance_email_id = serializers.EmailField(required=False, allow_blank=True, allow_null=True)
    email_for_receiving_po = serializers.EmailField(required=False, allow_blank=True, allow_null=True)
    email_id_for_quote = serializers.EmailField(required=False, allow_blank=True, allow_null=True)
    is_delete = serializers.BooleanField(required=False, allow_null=True)
    order_by = serializers.CharField(required=False, allow_blank=True, allow_null=True, write_only=True)
    order_type = serializers.CharField(required=False, allow_blank=True, allow_null=True, write_only=True)
    page = serializers.IntegerField(required=False, write_only=True, allow_null=True)
    page_size = serializers.IntegerField(required=False, write_only=True, allow_null=True)

    class Meta:
        model = SupplierContactDetails
        fields = ('contact_person', 'main_phone_number', 'main_email_id', 'finance_phone_number',
                  'finance_email_id', 'remittance_email_id', 'email_for_receiving_po',
                  'email_id_for_quote', 'is_delete', 'order_by', 'order_type', 'page', 'page_size')


class SupplierContactDetailsReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupplierContactDetails
        fields = ('id', 'contact_person', 'main_phone_number', 'main_email_id', 'finance_phone_number',
                  'finance_email_id', 'remittance_email_id', 'email_for_receiving_po',
                  'email_id_for_quote', 'created_by', 'updated_by', 'created_on', 'updated_on')
        read_only_fields = ('created_by', 'updated_by', 'created_on', 'updated_on')


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'
        read_only_fields = ('created_on', 'updated_on')


class CountryReadSerializer(serializers.ModelSerializer):
    created_by = serializers.SerializerMethodField(read_only=True)
    updated_by = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Country
        fields = (
            "id", "country_name", "country_code", "description", "created_by",
            "updated_by", "created_on", "updated_on", "is_active"
        )

    def get_created_by(self, obj):
        data = User.objects.filter(id=obj.created_by).first()
        if data:
            return f"{data.first_name} {data.last_name}".strip()
        else:
            return None

    def get_updated_by(self, obj):
        data = User.objects.filter(id=obj.updated_by).first()
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
    updated_on = serializers.DateTimeField(allow_null=True, required=False)
    updated_by = serializers.IntegerField(allow_null=True, required=False)
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
        read_only_fields = ('created_on', 'updated_on',)


class CurrencyReadSerializer(serializers.ModelSerializer):
    created_by = serializers.SerializerMethodField(read_only=True)
    updated_by = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Currency
        fields = (
            "id", "currency_name", "currency_code", "created_by",
            "updated_by", "created_on", "updated_on", "is_active"
        )

    def get_created_by(self, obj):
        data = User.objects.filter(id=obj.created_by).first()
        if data:
            return f"{data.first_name} {data.last_name}".strip()
        else:
            return None

    def get_updated_by(self, obj):
        data = User.objects.filter(id=obj.updated_by).first()
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
    updated_on = serializers.DateTimeField(allow_null=True, required=False)
    updated_by = serializers.IntegerField(allow_null=True, required=False)
    is_active = serializers.BooleanField(allow_null=True, required=False)
    order_by = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    order_type = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    export = serializers.BooleanField(required=False, allow_null=True, default=False)
    page = serializers.IntegerField(required=False, allow_null=True)
    page_size = serializers.IntegerField(required=False, allow_null=True)


class CategorySerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(source='created_by.first_name', required=False, read_only=True)
    updated_by = serializers.CharField(source='updated_by.first_name', required=False, read_only=True)

    class Meta:
        model = Category
        fields = ("id", "name", "updated_on", "updated_by", "created_at",
                  "created_by")
        read_only_fields = ('created_by', 'updated_by', 'created_at', 'updated_on', 'deleted_at')


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
    updated_by = serializers.CharField(source='updated_by.first_name', required=False, read_only=True)

    class Meta:
        model = Department
        fields = "__all__"
        read_only_fields = ('created_by', 'updated_by', 'is_delete', 'updated_on', 'deleted_at')

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
    updated_by = serializers.SerializerMethodField(source='get_updated_by')

    class Meta:
        model = Department
        fields = ('id', 'department_name', 'is_active', 'created_by', 'updated_by', 'created_at', 'updated_on')
        read_only_fields = ('updated_on', 'is_delete')

    def get_updated_by(self, obj):
        if obj.updated_by:
            return obj.updated_by.first_name
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
        read_only_fields = ('created_by', 'updated_by', 'is_delete')


class StatusSerializer(serializers.ModelSerializer):
    """
    This serializer is used to create and update the status.
    """

    created_by = serializers.SerializerMethodField(source='get_created_by')
    updated_by = serializers.SerializerMethodField(source='get_updated_by')

    class Meta:
        model = Status
        fields = '__all__'
        read_only_fields = ('created_by', 'updated_by', 'created_at', 'updated_at', 'deleted_at')

    def get_created_by(self, obj):
        return obj.created_by.first_name if obj.created_by else None

    def get_updated_by(self, obj):
        return obj.updated_by.first_name if obj.updated_by else None


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
    updated_by = serializers.SerializerMethodField(source='get_updated_by', required=False)

    # created_by = serializers.SerializerMethodField(required=False,)

    # export = serializers.BooleanField(required=False, allow_null=True, default=False)

    class Meta:
        model = Status
        fields = '__all__'
        read_only_fields = ('created_by', 'updated_by', 'created_at', 'updated_at', 'deleted_at')

    def get_created_by(self, obj):
        return obj.created_by.first_name if obj.created_by else None

    def get_updated_by(self, obj):
        return obj.updated_by.first_name if obj.updated_by else None


class StatusReadSerializer(serializers.ModelSerializer):
    """
    This serializer is used for response data of Status
    """
    created_by = serializers.SerializerMethodField(source='get_created_by', read_only=True)
    updated_by = serializers.SerializerMethodField(source='get_updated_by', read_only=True)

    class Meta:
        model = Status
        fields = (
            "id", "name", "status_code", "color_code", "highlight", "updated_at", "updated_by",
            "created_at", "created_by")

    def get_updated_by(self, obj):
        data = User.objects.filter(id=obj.updated_by).first()
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
        read_only_fields = ['created_by', 'created_on', 'updated_on', 'updated_by']

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
        data = super().to_internal_value(data)
        data['cc'] = ','.join(data['cc']) if isinstance(data['cc'], list) else data['cc']
        data['bcc'] = ','.join(data['bcc']) if isinstance(data['bcc'], list) else data['bcc']
        return data


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
    updated_by = serializers.SerializerMethodField()

    class Meta:
        model = EmailTemplate
        fields = (
        'id', 'template_type', 'subject', 'email_to', 'cc', 'bcc', 'message', 'signature', 'is_active', 'created_by',
        'updated_by', 'created_on', 'updated_on')
        read_only_fields = ('created_on', 'updated_on')

    def get_updated_by(self, obj):
        if obj.updated_by:
            return obj.updated_by.first_name
        return None
