from rest_framework import serializers
from .models import Department, SLA, Status, Category, ProjectManagement, TicketType, TicketRevision, TicketFollower, \
    Ticket, TicketBehalf, UserDepartment, Priority
from django.contrib.auth import get_user_model

User = get_user_model()


class SLAUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SLA
        fields = '__all__'


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = "__all__"
        read_only_fields = ('created_by', 'updated_by', 'is_delete')


class SLASerializer(serializers.ModelSerializer):
    class Meta:
        model = SLA
        fields = "__all__"
        read_only_fields = ('created_by', 'is_delete', 'updated_by', 'created_at', 'updated_at', 'deleted_at')

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
        fields = ('id', 'name', 'order_by', 'order_type', 'page', 'page_size')




class UserDepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDepartment
        fields = "__all__"
        read_only_fields = ('created_by', 'updated_by', 'is_delete')


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
    name = serializers.CharField(source='department_name', required=False)
    order_by = serializers.CharField(required=False, allow_blank=True, allow_null=True, write_only=True)
    order_type = serializers.CharField(required=False, allow_blank=True, allow_null=True, write_only=True)
    page = serializers.IntegerField(required=False, write_only=True, allow_null=True)
    page_size = serializers.IntegerField(required=False, write_only=True, allow_null=True)

    # export = serializers.BooleanField(required=False, allow_null=True, default=False)

    class Meta:
        model = Department
        fields = ('id', 'is_active', 'name', 'order_by', 'order_type', 'page', 'page_size')
        read_only_fields = ('department_type',)


class TicketTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketType
        fields = ('id', 'name', 'is_active', 'created_by')
        read_only_fields = ('created_at', 'updated_by', 'updated_at', 'deleted_at')


class TicketTypeUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketType
        fields = ('name', 'is_active')
        read_only_fields = ('created_by', 'created_at', 'updated_by', 'updated_at', 'deleted_at')


class TicketBehalfSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketBehalf
        fields = (
            'id', 'ticket_id', 'behalf_email', 'created_by', 'created_at', 'updated_by', 'updated_at', 'deleted_at')
        read_only_fields = ('created_by', 'created_at', 'updated_by', 'updated_at', 'deleted_at')


class TicketBehalfUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketBehalf
        fields = ('behalf_email',)
        read_only_fields = ('created_by', 'created_at', 'updated_by', 'updated_at', 'deleted_at')


class TicketBehalfFilterSerializer(serializers.ModelSerializer):
    ticket_id = serializers.IntegerField(required=False, allow_null=True)
    behalf_email = serializers.CharField(max_length=100, required=False, allow_blank=True, allow_null=True)
    created_at = serializers.DateTimeField(allow_null=True, required=False)
    created_by = serializers.IntegerField(allow_null=True, required=False)
    updated_at = serializers.DateTimeField(allow_null=True, required=False)
    updated_by = serializers.IntegerField(allow_null=True, required=False)
    order_by = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    order_type = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    page = serializers.IntegerField(required=False, allow_null=True)
    per_page = serializers.IntegerField(required=False, allow_null=True)
    export = serializers.BooleanField(required=False, allow_null=True, default=False)

    class Meta:
        model = TicketBehalf
        fields = (
            'ticket_id', 'behalf_email', 'created_at', 'created_by', 'updated_at', 'updated_by', 'order_by',
            'order_type', 'page', 'per_page', 'export')


class TicketFollowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketFollower
        fields = (
            'id', 'ticket_id', 'follower_id', 'created_by', 'created_at', 'updated_by', 'updated_at', 'deleted_at')
        read_only_fields = ('created_by', 'created_at', 'updated_by', 'updated_at', 'deleted_at')


class TicketFollowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketFollower
        fields = (
            'id', 'ticket_id', 'follower_id', 'created_by', 'created_at', 'updated_by', 'updated_at', 'deleted_at')
        read_only_fields = ('created_by', 'created_at', 'updated_by', 'updated_at', 'deleted_at')


class TicketFollowerUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketFollower
        fields = ('follower_id',)
        read_only_fields = ('created_by', 'created_at', 'updated_by', 'updated_at', 'deleted_at')


class TicketFollowerFilterSerializer(serializers.ModelSerializer):
    ticket_id = serializers.IntegerField(required=False, allow_null=True)
    follower_id = serializers.IntegerField(required=False, allow_null=True)
    created_at = serializers.DateTimeField(allow_null=True, required=False)
    created_by = serializers.IntegerField(allow_null=True, required=False)
    updated_at = serializers.DateTimeField(allow_null=True, required=False)
    updated_by = serializers.IntegerField(allow_null=True, required=False)
    order_by = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    order_type = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    page = serializers.IntegerField(required=False, allow_null=True)
    per_page = serializers.IntegerField(required=False, allow_null=True)
    export = serializers.BooleanField(required=False, allow_null=True, default=False)

    class Meta:
        model = TicketFollower
        fields = (
            'id', 'ticket_id', 'follower_id', 'created_at', 'created_by', 'updated_at', 'updated_by', 'order_by',
            'order_type', 'page', 'per_page', 'export')


class TicketRevisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketRevision
        fields = (
            'id', 'ticket_id', 'revision_status', 'pti', 'action_taken', 'before_revision', 'after_revision',
            'created_by',
            'created_at', 'updated_by', 'updated_at', 'deleted_at')
        read_only_fields = ('created_by', 'created_at', 'updated_by', 'updated_at', 'deleted_at')


class TicketRevisionUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketRevision
        fields = ('revision_status', 'pti', 'action_taken', 'before_revision', 'after_revision')
        read_only_fields = ('created_by', 'created_at', 'updated_by', 'updated_at', 'deleted_at')


class TicketRevisionFilterSerializer(serializers.ModelSerializer):
    ticket_id = serializers.IntegerField(required=False, allow_null=True)
    revision_status = serializers.IntegerField(required=False, allow_null=True)
    pti = serializers.IntegerField(required=False, allow_null=True)
    action_taken = serializers.DateTimeField(allow_null=True, required=False)
    before_revision = serializers.CharField(max_length=500, required=False, allow_blank=True, allow_null=True)
    after_revision = serializers.CharField(max_length=500, required=False, allow_blank=True, allow_null=True)
    created_at = serializers.DateTimeField(allow_null=True, required=False)
    created_by = serializers.IntegerField(allow_null=True, required=False)
    updated_at = serializers.DateTimeField(allow_null=True, required=False)
    updated_by = serializers.IntegerField(allow_null=True, required=False)
    order_by = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    order_type = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    page = serializers.IntegerField(required=False, allow_null=True)
    per_page = serializers.IntegerField(required=False, allow_null=True)
    export = serializers.BooleanField(required=False, allow_null=True, default=False)

    class Meta:
        model = TicketRevision
        fields = (
            'ticket_id', 'revision_status', 'pti', 'action_taken', 'before_revision', 'after_revision',
            'created_at', 'created_by', 'updated_at', 'updated_by', 'order_by', 'order_type', 'page', 'per_page',
            'export')


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'
        read_only_fields = ('created_by', 'updated_by', 'created_at', 'updated_at', 'deleted_at')


class TicketUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = (
            'ticket_no', 'ticket_status', 'ticket_header', 'ticket_details', 'on_behalf', 'ticket_category',
            'ticket_type',
            'department_id', 'project_id', 'ticket_priority', 'assigned_to', 'assigned_by', 'assigned_at',
            'reassigned_reason', 'reassigned_by', 'reassigned_at', 'reassigned_status', 'hold_from', 'hold_to',
            'cancellation_at', 'response_within', 'response_at', 'response_by', 'response_status', 'response_breach',
            'response_breach_time', 'resolution_within', 'resolution_postponed_time', 'resolution_at', 'resolution_by',
            'resolution_status', 'resolution_breach', 'resolution_breach_time', 'closed_at', 'comments', 'tags',
            'is_delete'
        )
        read_only_fields = ('created_by', 'created_at', 'updated_by', 'updated_at', 'deleted_at')


class TicketFilterSerializer(serializers.ModelSerializer):
    ticket_no = serializers.CharField(max_length=10, required=False, allow_blank=True, allow_null=True)
    ticket_status = serializers.IntegerField(required=False, allow_null=True)
    ticket_category = serializers.IntegerField(required=False, allow_null=True)
    ticket_type = serializers.IntegerField(required=False, allow_null=True)
    department_id = serializers.IntegerField(required=False, allow_null=True)
    project_id = serializers.IntegerField(required=False, allow_null=True)
    ticket_priority = serializers.IntegerField(required=False, allow_null=True)
    created_at = serializers.DateTimeField(allow_null=True, required=False)
    created_by = serializers.IntegerField(allow_null=True, required=False)
    updated_at = serializers.DateTimeField(allow_null=True, required=False)
    updated_by = serializers.IntegerField(allow_null=True, required=False)
    order_by = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    order_type = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    page = serializers.IntegerField(required=False, allow_null=True)
    per_page = serializers.IntegerField(required=False, allow_null=True)
    export = serializers.BooleanField(required=False, allow_null=True, default=False)

    class Meta:
        model = Ticket
        fields = (
            'ticket_no', 'ticket_status', 'ticket_category', 'ticket_type', 'department_id', 'project_id',
            'ticket_priority',
            'created_at', 'created_by', 'updated_at', 'updated_by', 'order_by', 'order_type', 'page', 'per_page',
            'export')


class PrioritySerializer(serializers.ModelSerializer):
    class Meta:
        model = Priority
        fields = '__all__'