from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db import transaction

from master_data_management.models import Client
from .models import (Role, RolePermission, MasterPrivilege, ClientPrivilege, AppConfiguration, )

User = get_user_model()


class RolePermissionSerializer(serializers.ModelSerializer):
    """
    This serializer is used for retrieving role permission
    """
    privilege_name = serializers.CharField(source='privilege.privilege_name')
    privilege_desc = serializers.CharField(source='privilege.privilege_desc')

    class Meta:
        model = RolePermission
        fields = ("id", "privilege_name", 'privilege_desc')


class RoleFilterSerializer(serializers.ModelSerializer):
    """
    This serializer is used for role filter
    """
    role_name = serializers.CharField(max_length=100, required=False, allow_blank=True, allow_null=True)
    role_description = serializers.CharField(max_length=200, required=False, allow_blank=True, allow_null=True)
    client_id = serializers.CharField(max_length=200, required=False, allow_blank=True, allow_null=True)
    include_privilege_data = serializers.BooleanField(default=True, required=False, allow_null=True)
    order_by = serializers.CharField(required=False, allow_blank=True, allow_null=True, write_only=True)
    order_type = serializers.CharField(required=False, allow_blank=True, allow_null=True, write_only=True)
    page = serializers.IntegerField(required=False, write_only=True, allow_null=True)
    page_size = serializers.IntegerField(required=False, write_only=True, allow_null=True)
    export = serializers.BooleanField(required=False, allow_null=True, default=False)

    class Meta:
        model = Role
        fields = (
            'role_name', 'role_description', 'client_id', 'include_privilege_data', 'order_by', "export",
            'order_type', 'page', 'page_size')


class RolePermissionFilterSerializer(serializers.ModelSerializer):
    """
    This serializer is used for making post request for  role permission
    """

    privilege_name = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    privilege_desc = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    role_id = serializers.IntegerField(required=False, allow_null=True)
    order_by = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    order_type = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    page = serializers.IntegerField(required=False, allow_null=True)
    page_size = serializers.IntegerField(required=False, allow_null=True)

    class Meta:
        model = RolePermission
        fields = ('privilege_name', 'privilege_desc', 'role_id', 'order_by', 'order_type', 'page', 'page_size')


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MasterPrivilege
        fields = ("id", "privilege_name", "privilege_desc", "module_id")


class RoleReadSerializer(serializers.ModelSerializer):
    privilege_names = serializers.SerializerMethodField()
    created_by = serializers.CharField(source='created_by.first_name')
    updated_by = serializers.CharField(source='updated_by.first_name', allow_null=True)

    class Meta:
        model = Role
        fields = "__all__"

    def get_privilege_names(self, obj):
        privileges = RolePermission.objects.filter(role=obj).select_related('privilege')
        return [privilege.privilege.privilege_name for privilege in privileges]

    # def get_updated_by(self, obj):
    #     data = User.objects.filter(id=obj.updated_by).first()
    #     if data:
    #         return f"{data.first_name} {data.last_name}".strip()
    #     else:
    #         return None


class RoleReadWithoutPrivilegeSerializer(serializers.ModelSerializer):
    """
    This serializer is used for response data of role
    """

    class Meta:
        model = Role
        fields = ("id", "role_name", "role_description", "client_id", "updated_on", "updated_by", "created_on",
                  "created_by", "is_active")


class RoleShortInfoSerializer(serializers.ModelSerializer):
    """
        This serializer is used for response data of role
        """

    class Meta:
        model = Role
        fields = ("id", "role_name", "role_description", "client_id")


class RoleSerializer(serializers.ModelSerializer):
    """
    This serializer is used for create and update the role
    """
    privilege_names = serializers.ListField(child=serializers.CharField(), write_only=True)
    role_name = serializers.CharField()
    role_description = serializers.CharField(max_length=1000, required=False, allow_null=True, allow_blank=True)
    is_active = serializers.BooleanField(default=True, required=False)

    class Meta:
        model = Role
        fields = ("id", "role_name", "role_description", "client_id", "privilege_names", "is_active")
        read_only_fields = ["created_by"]

    def create(self, validate_data):
        """
        This is a Create method for Role Create
        It takes role id, role name, role description, privilege id and return the Role object and privilege ids
        if everything is right otherwise it will return error
        """
        try:
            privilege_names = validate_data.pop("privilege_names", [])
            with transaction.atomic():

                instance = Role.objects.create(role_name=validate_data.get("role_name"),
                                               role_description=validate_data.get("role_description"),
                                               client_id=validate_data.get("client_id"),
                                               created_by=validate_data.get("created_by"))
                if MasterPrivilege.objects.filter(privilege_name__in=privilege_names).count() != len(
                        set(privilege_names)):
                    raise serializers.ValidationError("please provide valid privilege")
                for privilege_name in privilege_names:
                    privilege = MasterPrivilege.objects.filter(privilege_name=privilege_name).first()
                    RolePermission.objects.create(privilege=privilege, role=instance)

                instance.save()
                return instance
        except serializers.ValidationError as ve:
            raise serializers.ValidationError(ve.detail)
        except Exception as ee:
            raise serializers.ValidationError("Role name must be unique")

    def update(self, instance, validated_data):
        """
        This is an Update method for Role Update.
        It takes role id, role name, role description, privilege id and returns the Role object and privilege ids
        if everything is right; otherwise, it will return an error.
        """
        try:
            privilege_names = validated_data.pop('privilege_names', [])

            # Call the parent class's update method to handle the standard update logic
            record = super().update(instance, validated_data)

            # Check if the provided privileges are valid
            if MasterPrivilege.objects.filter(privilege_name__in=privilege_names).count() != len(set(privilege_names)):
                raise serializers.ValidationError("Please provide valid privilege")

            # Get existing privileges for the role
            existing_privileges = list(
                RolePermission.objects.filter(role=record).values_list("privilege__privilege_name", flat=True))
            existing_privileges.sort()
            privilege_names.sort()
            if existing_privileges != privilege_names:
                with transaction.atomic():
                    RolePermission.objects.filter(role=record).delete()
                    for privilege_name in privilege_names:
                        privilege = MasterPrivilege.objects.filter(privilege_name=privilege_name).first()
                        RolePermission.objects.create(privilege=privilege, role=record)

            return record

        except serializers.ValidationError as ve:
            raise serializers.ValidationError(ve.detail)
        except Exception as e:
            raise serializers.ValidationError("Please provide valid Role and privilege data")


class RoleMultiUserCreateSerializer(serializers.Serializer):
    role_id = serializers.CharField(max_length=100)
    user_ids = serializers.ListField(child=serializers.IntegerField(), required=True)


class ClientPrivilegeSerializer(serializers.ModelSerializer):
    """
    This serializer is used for create and update the role
    """

    class Meta:
        model = ClientPrivilege
        fields = ("id", "privilege", "client", "created_by", "created_on", "updated_by", "updated_on")
        read_only_fields = ("created_by", "created_on", "updated_by", "updated_on")


class ClientPrivilegeReadSerializer(serializers.ModelSerializer):
    """
    This serializer is used for response data of role
    """
    privilege = serializers.SerializerMethodField(source='get_privilege', read_only=True)
    client = serializers.SerializerMethodField(source='get_client', read_only=True)

    class Meta:
        model = ClientPrivilege
        fields = ("id", "privilege", "client", "created_by", "created_on", "updated_by", "updated_on")

    def get_privilege(self, obj):
        try:
            privilege = MasterPrivilege.objects.get(id=obj.privilege)
            return {
                'id': privilege.id,
                'name': privilege.privilege_name
            }
        except Exception as ee:
            return []

    def get_client(self, obj):
        try:
            client = Client.objects.get(id=obj.client)
            return {
                'id': client.id,
                'name': client.name
            }
        except Exception as ee:
            return []


class ClientPrivilegeFilterSerializer(serializers.ModelSerializer):
    """
    This serializer is used for client privilege filter
    """
    privilege = serializers.CharField(max_length=100, required=False, allow_blank=True, allow_null=True)
    client = serializers.CharField(max_length=200, required=False, allow_blank=True, allow_null=True)
    order_by = serializers.CharField(required=False, allow_blank=True, allow_null=True, write_only=True)
    order_type = serializers.CharField(required=False, allow_blank=True, allow_null=True, write_only=True)
    page = serializers.IntegerField(required=False, write_only=True, allow_null=True)
    page_size = serializers.IntegerField(required=False, write_only=True, allow_null=True)
    export = serializers.BooleanField(required=False, allow_null=True, default=False)

    class Meta:
        model = ClientPrivilege
        fields = (
            'privilege', 'client', 'order_by', "export", 'order_type', 'page', 'page_size')


class AppConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppConfiguration
        fields = '__all__'
        read_only_fields = ('created_by', 'created_on', 'updated_by', 'updated_on')

    def validate_application_name(self, value):
        # Check if an instance with the same application_name already exists
        if AppConfiguration.objects.filter(application_name=value).exists():
            raise serializers.ValidationError("Application name must be unique.")
        return value

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
