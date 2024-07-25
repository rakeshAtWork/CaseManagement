from rest_framework import serializers
from .models import Department, SLA, Status, Category, ProjectManagement
from django.contrib.auth import get_user_model

User = get_user_model()


class SLAUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SLA
        fields = ('department', 'ticket_type', 'priority', 'response_time', 'resolution_time', 'is_delete')
        read_only_fields = ('created_by', 'updated_by', 'created_at', 'updated_at', 'deleted_at')


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = "__all__"
        read_only_fields = ('created_by', 'updated_by', 'is_delete')


class SLASerializer(serializers.ModelSerializer):
    class Meta:
        model = SLA
        exclude = ['id']

    def create(self, validated_data):
        # Custom create method if needed
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Custom update method if needed
        return super().update(instance, validated_data)


class StatusSerializer(serializers.ModelSerializer):
    """
        This serializer is used for create and update the status
        """

    class Meta:
        model = Status
        fields = '__all__'
        read_only_fields = ('created_by', 'updated_by', 'created_at', 'updated_at', 'deleted_at')


class StatusFilterSerializer(serializers.ModelSerializer):
    """
    This serializer is used for status filter
    """
    # name = serializers.CharField(max_length=100, required=False, allow_blank=True, allow_null=True)
    order_by = serializers.CharField(required=False, allow_blank=True, allow_null=True, write_only=True)
    order_type = serializers.CharField(required=False, allow_blank=True, allow_null=True, write_only=True)
    page = serializers.IntegerField(required=False, write_only=True, allow_null=True)
    page_size = serializers.IntegerField(required=False, write_only=True, allow_null=True)

    # export = serializers.BooleanField(required=False, allow_null=True, default=False)

    class Meta:
        model = Status
        fields = '__all__'
        # ('name', 'status_code ', 'color_code', 'highlight','order_type','order_by','page','page_size')


class StatusReadSerializer(serializers.ModelSerializer):
    """
    This serializer is used for response data of Status
    """
    created_by = serializers.SerializerMethodField(source='get_created_by', read_only=True)
    updated_by = serializers.SerializerMethodField(source='get_modified_by', read_only=True)

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


class CategoryReadSerializer(serializers.ModelSerializer):
    """
    This serializer is used for response data of Category
    """
    created_by = serializers.SerializerMethodField(source='get_created_by', read_only=True)
    updated_by = serializers.SerializerMethodField(source='get_modified_by', read_only=True)

    class Meta:
        model = Category
        fields = ("id", "name", "updated_at", "updated_by", "created_at",
                  "created_by")

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


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name", "updated_at", "updated_by", "created_at",
                  "created_by")
        read_only_fields = ('created_by', 'updated_by', 'created_at', 'updated_at', 'deleted_at')


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
        fields = ('name', 'order_by', 'order_type', 'page', 'page_size')


class ProjectManagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectManagement
        fields = (
            "id", "client_id", "department_id", "project_id", "project_manager_primary",
            "support_group_email", "product_owner", "is_active", "contact_name", "contact_email")
        read_only_fields = ("created_at", "updated_at", "created_by", "updated_by", "deleted_at")


class ProjectManagementReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectManagement
        fields = (
            "id", "client_id", "department_id", "project_id", "project_manager_primary",
            "support_group_email", "product_owner", "is_active", "contact_name", "contact_email",
            "created_at", "updated_at", "created_by", "updated_by", "deleted_at")


class ProjectFilterSerializers(serializers.Serializer):
    id = serializers.IntegerField(allow_null=True, required=False)
    client_id = serializers.IntegerField(allow_null=True, required=False)
    client_name = serializers.CharField(allow_null=True, required=False)
    department_id = serializers.IntegerField(allow_null=True, required=False)
    project_id = serializers.IntegerField(allow_null=True, required=False)
    contact_name = serializers.CharField(allow_null=True, required=False)
    project_name = serializers.CharField(allow_null=True, required=False)
    project_manager_primary = serializers.IntegerField(allow_null=True, required=False)
    support_group_email = serializers.CharField(allow_null=True, required=False)
    product_owner = serializers.CharField(allow_null=True, required=False)
    contact_email = serializers.CharField(allow_null=True, required=False)
    is_active = serializers.BooleanField(allow_null=True, required=False)
    created_at = serializers.DateTimeField(allow_null=True, required=False)
    updated_at = serializers.DateTimeField(allow_null=True, required=False)
    deleted_at = serializers.DateTimeField(allow_null=True, required=False)
    order_by = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    created_by = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    updated_by = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    order_type = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    page = serializers.IntegerField(required=False, allow_null=True)
    page_size = serializers.IntegerField(required=False, allow_null=True)
    export = serializers.BooleanField(required=False, allow_null=True, default=False)

    class Meta:
        model = ProjectManagement
        fields = (
            "id", "client_id", "client_name", "department_id", "project_id", "project_name", "project_manager_primary",
            "support_group_email", "product_owner", "is_active", "contact_name", "contact_email",
            "created_at", "updated_at", "created_by", "updated_by", "deleted_at")


class DepartmentFilterSerializer(serializers.ModelSerializer):
    """
    This serializer is used for department filter
    """
    name = serializers.CharField(max_length=100, required=False, allow_blank=True, allow_null=True)
    order_by = serializers.CharField(required=False, allow_blank=True, allow_null=True, write_only=True)
    order_type = serializers.CharField(required=False, allow_blank=True, allow_null=True, write_only=True)
    page = serializers.IntegerField(required=False, write_only=True, allow_null=True)
    page_size = serializers.IntegerField(required=False, write_only=True, allow_null=True)

    # export = serializers.BooleanField(required=False, allow_null=True, default=False)

    class Meta:
        model = Department
        fields = ('department_name', 'department_code', 'department_type', 'is_active')
