from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db import transaction

from master_data_management.models import Client
from .models import (Role, RolePermission, UserRole, MasterPrivilege, ClientPrivilege, )

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
    include_privilege_data = serializers.BooleanField(default=False, required=False, allow_null=True)
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
        fields = ("id", "privilege_name", "privilege_desc")


# class RoleUserSerializer(serializers.ModelSerializer):
#     role_name = serializers.SerializerMethodField(source='get_role_name', read_only=True)
#     role_id = serializers.IntegerField(required=True)
#     user_id = serializers.IntegerField(required=True)
#
#     class Meta:
#         model = UserRole
#         fields = ("id", "user_id", "role_id", "role_name")
#
#     def get_role_name(self, obj):
#         return obj.role.role_name
#
#     def create(self, validated_data):
#         role_id = validated_data.pop("role_id")
#         user_id = validated_data.pop("user_id")
#         role = Role.objects.filter(id=role_id).first()
#         user = User.objects.filter(id=user_id).first()
#         if not role and not user:
#             raise serializers.ValidationError("role id or user id is not valid")
#
#         validated_data["role"] = role
#         validated_data["user"] = user
#         instance = super(RoleUserSerializer, self).create(validated_data)
#         return instance


# class RoleReadSerializer(serializers.ModelSerializer):
#     """
#     This serializer is used for response data of role
#     """
#     privilege_names = serializers.SerializerMethodField(source='get_privilege_names', read_only=True)
#
#     class Meta:
#         model = Role
#         fields = ("id", "role_name", "role_description", "client_id", "privilege_names", "modified_on", "modified_by",
#                   "created_on",
#                   "created_by")
#
#     def get_privilege_names(self, obj):
#         permissions = RolePermission.objects.filter(role=obj).values_list("privilege", flat=True)
#         return PermissionSerializer(MasterPrivilege.objects.filter(id__in=permissions), read_only=True,
#                                     context=self.context, many=True).data
class RoleReadSerializer(serializers.ModelSerializer):
    privilege_names = serializers.SerializerMethodField()

    class Meta:
        model = Role
        fields = ("id", "role_name", "role_description", "client_id", "privilege_names")

    def get_privilege_names(self, obj):
        privileges = RolePermission.objects.filter(role=obj).select_related('privilege')
        return [privilege.privilege.privilege_name for privilege in privileges]


class RoleReadWithoutPrivilegeSerializer(serializers.ModelSerializer):
    """
    This serializer is used for response data of role
    """

    class Meta:
        model = Role
        fields = ("id", "role_name", "role_description", "client_id", "modified_on", "modified_by", "created_on",
                  "created_by")


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

    class Meta:
        model = Role
        fields = ("id", "role_name", "role_description", "client_id", "privilege_names")

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
                    RolePermission.objects.create(privilege=privilege, role=instance,
                                                  created_by=validate_data.get("created_by"))
                instance.save()
                return instance
        except serializers.ValidationError as ve:
            raise serializers.ValidationError(ve.detail)
        except Exception as ee:
            raise serializers.ValidationError("Role name must be unique")

    def update(self, instance, validate_data):
        """
        This is an Update method for Role Update
        It takes role id, role name, role description, privilege id and return the Role object and privilege ids
        if everything is right otherwise it will return error
        """
        try:
            privilege_names = validate_data.get('privilege_names', [])
            record = instance
            if MasterPrivilege.objects.filter(privilege_name__in=privilege_names).count() != len(set(privilege_names)):
                raise serializers.ValidationError("please provide valid privilege")
            role_data = RolePermission.objects.filter(role=record).values_list("privilege__privilege_name", flat=True)
            with transaction.atomic():
                role_data = list(role_data)
                role_data.sort()
                privilege_names.sort()
                if not role_data == privilege_names:
                    RolePermission.objects.filter(role=record).delete()
                    for privilege_name in privilege_names:
                        privilege = MasterPrivilege.objects.filter(privilege_name=privilege_name).first()
                        RolePermission.objects.create(privilege=privilege, role=instance,
                                                      created_by=validate_data.get("modified_by"))
                record.role_name = validate_data.get('role_name')
                record.role_description = validate_data.get('role_description')
                record.client_id = validate_data.get('client_id')
                record.modified_by = validate_data.get('modified_by')
                record.modified_on = timezone.now().astimezone(timezone.timezone.utc)
                record.save()
                return record
        except serializers.ValidationError as ve:
            raise serializers.ValidationError(ve.detail)
        except Exception:
            raise serializers.ValidationError("Please provide Valid Role and privilege data")


class RoleMultiUserCreateSerializer(serializers.Serializer):
    role_id = serializers.CharField(max_length=100)
    user_ids = serializers.ListField(child=serializers.IntegerField(), required=True)


class ClientPrivilegeSerializer(serializers.ModelSerializer):
    """
    This serializer is used for create and update the role
    """

    class Meta:
        model = ClientPrivilege
        fields = ("id", "privilege", "client", "created_by", "created_on", "modified_by", "modified_on")
        read_only_fields = ("created_by", "created_on", "modified_by", "modified_on")


class ClientPrivilegeReadSerializer(serializers.ModelSerializer):
    """
    This serializer is used for response data of role
    """
    privilege = serializers.SerializerMethodField(source='get_privilege', read_only=True)
    client = serializers.SerializerMethodField(source='get_client', read_only=True)

    class Meta:
        model = ClientPrivilege
        fields = ("id", "privilege", "client", "created_by", "created_on", "modified_by", "modified_on")

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
