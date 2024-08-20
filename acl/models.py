import logging
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
import uuid

User = get_user_model()
logger = logging.getLogger(name="CMS")


class Role(models.Model):
    """
    Role table
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role_name = models.CharField(max_length=50, unique=True)
    role_description = models.CharField(max_length=1000, db_column="role_desc", null=True, blank=True)
    client_id = models.CharField(max_length=1000, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE,
                                   related_name="role_created_by")
    updated_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE,
                                   related_name="role_update_by")
    is_active = models.BooleanField(default=True)
    updated_on = models.DateTimeField(null=True)

    objects = models.Manager()

    class Meta:
        ordering = ['-created_on']
        db_table = "ROLE"


class UserRole(models.Model):
    """
    Role Add to user
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="role_user")
    role = models.ForeignKey(Role, on_delete=models.CASCADE,
                             related_name="user_role_role")
    created_by = models.CharField(max_length=100)
    created_on = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    class Meta:
        ordering = ['-created_on']
        db_table = "USER_ROLE"


class MasterPrivilege(models.Model):
    """
    This model is the counterpart of the Permission.
     Allows storing a database counterpart of a permission.
    It is used to store the permissions help by a role or in an ACL.
    """
    namespace = models.CharField(max_length=64, verbose_name=_('Namespace'))
    privilege_name = models.CharField(max_length=50, verbose_name=_('Privilege'), unique=True)
    privilege_desc = models.CharField(max_length=1000, verbose_name=_('Privilege Description'))
    module_id = models.CharField(max_length=1000, verbose_name=_('Privilege Description'))
    is_active = models.BooleanField(default=True, verbose_name='active')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    class Meta:
        ordering = ('privilege_name',)
        db_table = "PRIVILEGE"


class RolePermission(models.Model):
    """
    Role Permission creation
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    privilege = models.ForeignKey(MasterPrivilege, on_delete=models.CASCADE, related_name="role_permission",
                                  db_column='privilege_id')
    role = models.ForeignKey(Role, on_delete=models.CASCADE,
                             related_name="role_permission_role", db_column='role_id')
    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE,
                                   related_name="role_privilege_created_by")
    created_on = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE,
                                   related_name="role_privilege_updated_by")
    updated_on = models.DateTimeField(null=True)

    objects = models.Manager()

    class Meta:
        ordering = ['-created_on']
        db_table = "ROLE_PERMISSIONS"


class ClientPrivilege(models.Model):
    """
    Client Privilege creation
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    privilege = models.PositiveIntegerField()
    client = models.CharField(max_length=100)
    created_by = models.CharField(max_length=100)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(null=True)
    updated_by = models.PositiveIntegerField(null=True)

    objects = models.Manager()

    class Meta:
        ordering = ['-created_on']
        db_table = "CLIENT_PRIVILEGE"


class AppConfiguration(models.Model):
    application_name = models.CharField(max_length=255)
    email_history_days = models.IntegerField()
    activity_history_days = models.IntegerField()
    client_start_no = models.CharField(max_length=100)
    project_start_no = models.CharField(max_length=100)
    ticket_start_no = models.CharField(max_length=100)
    ticket_auto_close_days = models.IntegerField()
    auto_notification_hours = models.IntegerField()
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100, blank=True, null=True)
    updated_on = models.DateTimeField(null=True, blank=True, )
    updated_by = models.CharField(max_length=100, null=True, blank=True)

    objects = models.Manager()

    class Meta:
        db_table = 'APP_CONFIGURATION'


class MasterModule(models.Model):
    MODULE_CHOICES = [
        (10, 'file_type_management'),
        (20, 'client_management'),
        (30, 'vendor_management'),
        (40, 'business_unit_management'),
        (50, 'application_management'),
        (60, 'account_type_management'),
        (70, 'd365fo_setup_management'),
        (80, 'supplier_management'),
        (90, 'carrier_consolidation_management'),
        (100, 'company_management'),
        (110, 'cpp_sanction_assessment_management'),
        (120, 'country_management'),
        (130, 'user_management'),
        (140, 'roles_management'),
        (150, 'currency_management'),
        (160, 'category_management'),
        (170, 'country_management'),
        (180, 'department_management'),
        (190, 'user_department_management'),
        (200, 'status_management'),
        (220, 'ticket_management'),
        (230, 'sla_management'),
        (240, 'customer_management'),
        (250, 'priority_management')
    ]

    module_id = models.PositiveIntegerField(choices=MODULE_CHOICES, primary_key=True)
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name
