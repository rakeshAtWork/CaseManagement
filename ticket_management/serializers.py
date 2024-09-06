from rest_framework import serializers

from master_data_management.models import Department
from .models import SLA
from django.contrib.auth import get_user_model
from master_data_management.serializers import DepartmentSerializer

User = get_user_model()


# class ProjectManagementSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ProjectManagement
#         fields = (
#             "id", "client_id", "department_id", "project_id", "project_manager_primary",
#             "support_group_email", "product_owner", "is_active", "contact_name", "contact_email")
#         read_only_fields = ("created_on", "modified_on", "created_by", "modified_by", "deleted_at")
#
#
# class ProjectManagementReadSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ProjectManagement
#         fields = (
#             "id", "client_id", "department_id", "project_id", "project_manager_primary",
#             "support_group_email", "product_owner", "is_active", "contact_name", "contact_email",
#             "created_on", "modified_on", "created_by", "modified_by", "deleted_at")
#
#
# class ProjectFilterSerializers(serializers.Serializer):
#     id = serializers.IntegerField(allow_null=True, required=False)
#     client_id = serializers.IntegerField(allow_null=True, required=False)
#     client_name = serializers.CharField(allow_null=True, required=False)
#     department_id = serializers.IntegerField(allow_null=True, required=False)
#     project_id = serializers.IntegerField(allow_null=True, required=False)
#     contact_name = serializers.CharField(allow_null=True, required=False)
#     project_name = serializers.CharField(allow_null=True, required=False)
#     project_manager_primary = serializers.IntegerField(allow_null=True, required=False)
#     support_group_email = serializers.CharField(allow_null=True, required=False)
#     product_owner = serializers.CharField(allow_null=True, required=False)
#     contact_email = serializers.CharField(allow_null=True, required=False)
#     is_active = serializers.BooleanField(allow_null=True, required=False)
#     created_on = serializers.DateTimeField(allow_null=True, required=False)
#     modified_on = serializers.DateTimeField(allow_null=True, required=False)
#     deleted_at = serializers.DateTimeField(allow_null=True, required=False)
#     order_by = serializers.CharField(required=False, allow_blank=True, allow_null=True)
#     created_by = serializers.CharField(required=False, allow_blank=True, allow_null=True)
#     modified_by = serializers.CharField(required=False, allow_blank=True, allow_null=True)
#     order_type = serializers.CharField(required=False, allow_blank=True, allow_null=True)
#     page = serializers.IntegerField(required=False, allow_null=True)
#     page_size = serializers.IntegerField(required=False, allow_null=True)
#     export = serializers.BooleanField(required=False, allow_null=True, default=False)
#
#     class Meta:
#         model = ProjectManagement
#         fields = (
#             "id", "client_id", "client_name", "department_id", "project_id", "project_name", "project_manager_primary",
#             "support_group_email", "product_owner", "is_active", "contact_name", "contact_email",
#             "created_on", "modified_on", "created_by", "modified_by", "deleted_at")
#
#
# class TicketTypeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = TicketType
#         fields = ('id', 'name', 'is_active')
#         read_only_fields = ('created_on', 'modified_by', 'modified_on', 'deleted_at')
#
#
# class TicketTypeUpdateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = TicketType
#         fields = ('name', 'is_active')
#         read_only_fields = ('created_by', 'created_on', 'modified_by', 'modified_on', 'deleted_at')
#
#
# class TicketBehalfSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = TicketBehalf
#         fields = (
#             'id', 'ticket_id', 'behalf_email', 'created_by', 'created_on', 'modified_by', 'modified_on', 'deleted_at')
#         read_only_fields = ('created_by', 'created_on', 'modified_by', 'modified_on', 'deleted_at')
#
#
# class TicketBehalfUpdateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = TicketBehalf
#         fields = ('behalf_email',)
#         read_only_fields = ('created_by', 'created_on', 'modified_by', 'modified_on', 'deleted_at')
#
#
# class TicketBehalfFilterSerializer(serializers.ModelSerializer):
#     ticket_id = serializers.IntegerField(required=False, allow_null=True)
#     behalf_email = serializers.CharField(max_length=100, required=False, allow_blank=True, allow_null=True)
#     created_on = serializers.DateTimeField(allow_null=True, required=False)
#     created_by = serializers.IntegerField(allow_null=True, required=False)
#     modified_on = serializers.DateTimeField(allow_null=True, required=False)
#     modified_by = serializers.IntegerField(allow_null=True, required=False)
#     order_by = serializers.CharField(required=False, allow_blank=True, allow_null=True)
#     order_type = serializers.CharField(required=False, allow_blank=True, allow_null=True)
#     page = serializers.IntegerField(required=False, allow_null=True)
#     per_page = serializers.IntegerField(required=False, allow_null=True)
#     export = serializers.BooleanField(required=False, allow_null=True, default=False)
#
#     class Meta:
#         model = TicketBehalf
#         fields = (
#             'ticket_id', 'behalf_email', 'created_on', 'created_by', 'modified_on', 'modified_by', 'order_by',
#             'order_type', 'page', 'per_page', 'export')
#
#
# class TicketFollowerSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = TicketFollower
#         fields = (
#             'id', 'ticket_id', 'follower_id', 'created_by', 'created_on', 'modified_by', 'modified_on', 'deleted_at')
#         read_only_fields = ('created_by', 'created_on', 'modified_by', 'modified_on', 'deleted_at')


# class TicketFollowerSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = TicketFollower
#         fields = (
#             'id', 'ticket_id', 'follower_id', 'created_by', 'created_on', 'modified_by', 'modified_on', 'deleted_at')
#         read_only_fields = ('created_by', 'created_on', 'modified_by', 'modified_on', 'deleted_at')


# class TicketFollowerUpdateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = TicketFollower
#         fields = ('follower_id',)
#         read_only_fields = ('created_by', 'created_on', 'modified_by', 'modified_on', 'deleted_at')
#
#
# class TicketFollowerFilterSerializer(serializers.ModelSerializer):
#     ticket_id = serializers.IntegerField(required=False, allow_null=True)
#     follower_id = serializers.IntegerField(required=False, allow_null=True)
#     created_on = serializers.DateTimeField(allow_null=True, required=False)
#     created_by = serializers.IntegerField(allow_null=True, required=False)
#     modified_on = serializers.DateTimeField(allow_null=True, required=False)
#     modified_by = serializers.IntegerField(allow_null=True, required=False)
#     order_by = serializers.CharField(required=False, allow_blank=True, allow_null=True)
#     order_type = serializers.CharField(required=False, allow_blank=True, allow_null=True)
#     page = serializers.IntegerField(required=False, allow_null=True)
#     per_page = serializers.IntegerField(required=False, allow_null=True)
#     export = serializers.BooleanField(required=False, allow_null=True, default=False)
#
#     class Meta:
#         model = TicketFollower
#         fields = (
#             'id', 'ticket_id', 'follower_id', 'created_on', 'created_by', 'modified_on', 'modified_by', 'order_by',
#             'order_type', 'page', 'per_page', 'export')
#
#
# class TicketRevisionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = TicketRevision
#         fields = (
#             'id', 'ticket_id', 'revision_status', 'pti', 'action_taken', 'before_revision', 'after_revision',
#             'created_by',
#             'created_on', 'modified_by', 'modified_on', 'deleted_at')
#         read_only_fields = ('created_by', 'created_on', 'modified_by', 'modified_on', 'deleted_at')
#
#
# class TicketRevisionUpdateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = TicketRevision
#         fields = ('revision_status', 'pti', 'action_taken', 'before_revision', 'after_revision')
#         read_only_fields = ('created_by', 'created_on', 'modified_by', 'modified_on', 'deleted_at')
#
#
# class TicketRevisionFilterSerializer(serializers.ModelSerializer):
#     ticket_id = serializers.IntegerField(required=False, allow_null=True)
#     revision_status = serializers.IntegerField(required=False, allow_null=True)
#     pti = serializers.IntegerField(required=False, allow_null=True)
#     action_taken = serializers.DateTimeField(allow_null=True, required=False)
#     before_revision = serializers.CharField(max_length=500, required=False, allow_blank=True, allow_null=True)
#     after_revision = serializers.CharField(max_length=500, required=False, allow_blank=True, allow_null=True)
#     created_on = serializers.DateTimeField(allow_null=True, required=False)
#     created_by = serializers.IntegerField(allow_null=True, required=False)
#     modified_on = serializers.DateTimeField(allow_null=True, required=False)
#     modified_by = serializers.IntegerField(allow_null=True, required=False)
#     order_by = serializers.CharField(required=False, allow_blank=True, allow_null=True)
#     order_type = serializers.CharField(required=False, allow_blank=True, allow_null=True)
#     page = serializers.IntegerField(required=False, allow_null=True)
#     per_page = serializers.IntegerField(required=False, allow_null=True)
#     export = serializers.BooleanField(required=False, allow_null=True, default=False)
#
#     class Meta:
#         model = TicketRevision
#         fields = (
#             'ticket_id', 'revision_status', 'pti', 'action_taken', 'before_revision', 'after_revision',
#             'created_on', 'created_by', 'modified_on', 'modified_by', 'order_by', 'order_type', 'page', 'per_page',
#             'export')
#
#
# class TicketSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Ticket
#         fields = '__all__'
#         read_only_fields = ('created_by', 'modified_by', 'created_on', 'modified_on', 'deleted_at')
#
#
# class TicketUpdateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Ticket
#         fields = (
#             'ticket_no', 'ticket_status', 'ticket_header', 'ticket_details', 'on_behalf', 'ticket_category',
#             'ticket_type',
#             'department_id', 'project_id', 'ticket_priority', 'assigned_to', 'assigned_by', 'assigned_at',
#             'reassigned_reason', 'reassigned_by', 'reassigned_at', 'reassigned_status', 'hold_from', 'hold_to',
#             'cancellation_at', 'response_within', 'response_at', 'response_by', 'response_status', 'response_breach',
#             'response_breach_time', 'resolution_within', 'resolution_postponed_time', 'resolution_at', 'resolution_by',
#             'resolution_status', 'resolution_breach', 'resolution_breach_time', 'closed_at', 'comments', 'tags',
#             'is_delete'
#         )
#         read_only_fields = ('created_by', 'created_on', 'modified_by', 'modified_on', 'deleted_at')
#
#
# class TicketFilterSerializer(serializers.ModelSerializer):
#     ticket_no = serializers.CharField(max_length=10, required=False, allow_blank=True, allow_null=True)
#     ticket_status = serializers.IntegerField(required=False, allow_null=True)
#     ticket_category = serializers.IntegerField(required=False, allow_null=True)
#     ticket_type = serializers.IntegerField(required=False, allow_null=True)
#     department_id = serializers.IntegerField(required=False, allow_null=True)
#     project_id = serializers.IntegerField(required=False, allow_null=True)
#     ticket_priority = serializers.IntegerField(required=False, allow_null=True)
#     created_on = serializers.DateTimeField(allow_null=True, required=False)
#     created_by = serializers.IntegerField(allow_null=True, required=False)
#     modified_on = serializers.DateTimeField(allow_null=True, required=False)
#     modified_by = serializers.IntegerField(allow_null=True, required=False)
#     order_by = serializers.CharField(required=False, allow_blank=True, allow_null=True)
#     order_type = serializers.CharField(required=False, allow_blank=True, allow_null=True)
#     page = serializers.IntegerField(required=False, allow_null=True)
#     per_page = serializers.IntegerField(required=False, allow_null=True)
#     export = serializers.BooleanField(required=False, allow_null=True, default=False)
#
#     class Meta:
#         model = Ticket
#         fields = (
#             'ticket_no', 'ticket_status', 'ticket_category', 'ticket_type', 'department_id', 'project_id',
#             'ticket_priority',
#             'created_on', 'created_by', 'modified_on', 'modified_by', 'order_by', 'order_type', 'page', 'per_page',
#             'export')
#
#
# class PrioritySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Priority
#         fields = '__all__'
#
#
# class TicketTypeFilterSerializer(serializers.ModelSerializer):
#     name = serializers.CharField(required=False, allow_blank=True, allow_null=True)
#     is_active = serializers.BooleanField(required=False, allow_null=True)
#     order_by = serializers.CharField(required=False, allow_blank=True, allow_null=True, write_only=True)
#     order_type = serializers.CharField(required=False, allow_blank=True, allow_null=True, write_only=True)
#     page = serializers.IntegerField(required=False, write_only=True, allow_null=True)
#     page_size = serializers.IntegerField(required=False, write_only=True, allow_null=True)
#
#     class Meta:
#         model = TicketType
#         fields = ('name', 'is_active', 'order_by', 'order_type', 'page', 'page_size')
#
#
# class TicketTypeReadSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = TicketType
#         fields = ('id', 'name', 'is_active')
#         read_only_fields = ('created_by', 'modified_by', 'created_on', 'modified_on')


class SLASerializer(serializers.ModelSerializer):
    class Meta:
        model = SLA
        fields = ['id', 'department', 'response_time', 'resolution_time']
        read_only_fields = ('created_by', 'modified_by', 'created_on', 'modified_on', "is_delete", "deleted_at")

    def create(self, validated_data):
        return SLA.objects.create(**validated_data)


class SLAUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SLA
        fields = '__all__'
        read_only_fields = ('created_by', 'modified_by', 'created_on', 'modified_on', "is_delete", "deleted_at")


class SLAFilterSerializer(serializers.ModelSerializer):
    department = serializers.IntegerField(required=False, allow_null=True)
    department_name = serializers.CharField(required=False, allow_null=True)
    # ticket_type = serializers.IntegerField(required=False, allow_null=True)
    # priority = serializers.IntegerField(required=False, allow_null=True)
    is_delete = serializers.BooleanField(required=False, allow_null=True)
    page = serializers.IntegerField(required=False, write_only=True, allow_null=True)
    page_size = serializers.IntegerField(required=False, write_only=True, allow_null=True)
    order_by = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    order_type = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    class Meta:
        model = SLA
        fields = ('department', 'department_name', 'is_delete', 'page', 'page_size', 'order_by', 'order_type')


class SLAReadSerializer(serializers.ModelSerializer):
    # department = serializers.CharField(source='department.department_name')
    department_details = serializers.SerializerMethodField(source='get_department_details', read_only=True)
    # ticket_type_details = serializers.SerializerMethodField(source='get_ticket_type_details', read_only=True)
    # priority_details = serializers.SerializerMethodField(source='get_priority_details', read_only=True)
    # ticket_type = serializers.CharField(source='ticket_type.name')
    # priority = serializers.CharField(source='priority.name')
    created_by = serializers.SerializerMethodField(source='get_created_by', read_only=True)
    modified_by = serializers.SerializerMethodField(source='get_updated_by', read_only=True)

    def get_department_details(self, obj):
        try:
            department = Department.objects.get(id=obj.department_id)
            return DepartmentSerializer(department).data
        except Department.DoesNotExist:
            return None

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

    class Meta:
        model = SLA
        fields = "__all__"
        read_only_fields = ('modified_on', 'modified_by', 'created_on', 'created_by', 'is_delete')
