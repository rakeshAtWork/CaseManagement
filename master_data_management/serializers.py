from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from rest_framework import serializers

from .models import FileType, Client, BusinessUnit, Vendor, Application, Customer

User = get_user_model()


class FileTypeSerializers(serializers.ModelSerializer):
    class Meta:
        model = FileType
        fields = (
            "id", "status", "file_type", "file_extension", "max_file_size", "file_description", "created_by",
            "modified_by", "created_on", "modified_on",)
        read_only_fields = ("created_by", "modified_by", "created_on", "modified_on")

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
    modified_by = serializers.SerializerMethodField(source='get_modified_by', read_only=True)

    class Meta:
        model = FileType
        fields = (
            "id", "status", "file_type", "file_extension", "max_file_size", "file_description", "created_by",
            "modified_by", "created_on", "modified_on", "is_delete")

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


class FileTypeFilterSerializers(serializers.Serializer):
    status = serializers.BooleanField(allow_null=True, required=False)
    file_type = serializers.CharField(allow_null=True, required=False)
    file_extension = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    max_file_size = serializers.IntegerField(allow_null=True, required=False)
    file_description = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    created_on = serializers.DateTimeField(allow_null=True, required=False)
    created_by = serializers.IntegerField(allow_null=True, required=False)
    modified_on = serializers.DateTimeField(allow_null=True, required=False)
    modified_by = serializers.IntegerField(allow_null=True, required=False)
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
            "created_by", "modified_by", "created_on", "modified_on")
        read_only_fields = ("created_by", "modified_by", "created_on", "modified_on")

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
    # modified_by = serializers.SerializerMethodField(source='get_modified_by', read_only=True)

    class Meta:
        model = Client
        fields = (
            "id", "status", "code", "name", "contact_name", "contact_email", "contact_number", "is_delete",
            "created_by", "modified_by", "created_on", "modified_on")

    # def get_modified_by(self, obj):
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
    modified_on = serializers.DateTimeField(allow_null=True, required=False)
    modified_by = serializers.IntegerField(allow_null=True, required=False)
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
            "created_by", "modified_by", "created_on", "modified_on")
        read_only_fields = ("created_by", "modified_by", "created_on", "modified_on")

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
            "created_by", "modified_by", "created_on", "modified_on")


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
    modified_on = serializers.DateTimeField(allow_null=True, required=False)
    modified_by = serializers.IntegerField(allow_null=True, required=False)
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
            "created_by", "modified_by", "created_on", "modified_on", "is_delete", "status")
        read_only_fields = ("created_by", "modified_by", "created_on", "modified_on")

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
            "created_by", "modified_by", "created_on", "modified_on", "is_delete", "status")

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
    modified_on = serializers.DateTimeField(allow_null=True, required=False)
    modified_by = serializers.IntegerField(allow_null=True, required=False)
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
            "created_by", "modified_by", "created_on", "modified_on")
        read_only_fields = ("created_by", "modified_by", "created_on", "modified_on")

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
            "contact_number", "created_by", "modified_by", "created_on", "modified_on")


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
    modified_on = serializers.DateTimeField(allow_null=True, required=False)
    modified_by = serializers.IntegerField(allow_null=True, required=False)
    order_by = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    order_type = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    export = serializers.BooleanField(required=False, allow_null=True, default=False)
    page = serializers.IntegerField(required=False, allow_null=True)
    page_size = serializers.IntegerField(required=False, allow_null=True)


class ApplicationSerializers(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = (
            "id", "status", "code", "name", "created_by", "modified_by", "created_on", "modified_on", "contact_name",
            "contact_email", "contact_number", "status")
        read_only_fields = ("created_by", "modified_by", "created_on", "modified_on")


class ApplicationReadSerializers(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = (
            "id", "status", "code", "name", "created_by", "modified_by", "created_on", "modified_on",
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
    modified_on = serializers.DateTimeField(allow_null=True, required=False)
    modified_by = serializers.IntegerField(allow_null=True, required=False)
    order_by = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    order_type = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    export = serializers.BooleanField(required=False, allow_null=True, default=False)
    page = serializers.IntegerField(required=False, allow_null=True)
    page_size = serializers.IntegerField(required=False, allow_null=True)
