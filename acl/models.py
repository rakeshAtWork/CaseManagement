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
    created_by = models.CharField(max_length=100)
    modified_by = models.PositiveIntegerField(null=True)

    modified_on = models.DateTimeField(null=True)

    objects = models.Manager()

    class Meta:
        ordering = ['-created_on']
        db_table = "ROLE"

    def __str__(self):
        return self.role_name


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

    def __str__(self):
        return self.privilege_name


class RolePermission(models.Model):
    """
    Role Permission creation
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    privilege = models.ForeignKey(MasterPrivilege, on_delete=models.CASCADE, related_name="role_permission",
                                  db_column='privilege_id')
    role = models.ForeignKey(Role, on_delete=models.CASCADE,
                             related_name="role_permission_role", db_column='role_id')
    created_by = models.CharField(max_length=100)
    created_on = models.DateTimeField(auto_now_add=True)

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
    modified_on = models.DateTimeField(null=True)
    modified_by = models.PositiveIntegerField(null=True)

    objects = models.Manager()

    class Meta:
        ordering = ['-created_on']
        db_table = "CLIENT_PRIVILEGE"


class AppConfiguration(models.Model):
    key = models.CharField(max_length=50)
    value = models.TextField()
    group = models.CharField(max_length=100, null=True, blank=True)
    application = models.CharField(max_length=100, null=True, blank=True)
    description = models.CharField(max_length=500, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100)
    modified_on = models.DateTimeField(null=True, blank=True)
    modified_by = models.CharField(max_length=100, null=True, blank=True)

    objects = models.Manager()

    class Meta:
        ordering = ['key']
        db_table = 'APP_CONFIGURATION'
