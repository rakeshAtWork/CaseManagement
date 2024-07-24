from django.apps import AppConfig
from django.db.utils import OperationalError, ProgrammingError


class AclConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'acl'
    #
    # def ready(self):
    #     self.create_permissions()  # Separate method for permissions
    #     # import master.signals  # Register signals
    #
    # def create_permissions(self):
    #     from .auth import create_permission
    #
    #     from .permissions import (
    #         permission_role_create,
    #         permission_role_list,
    #         permission_role_view,
    #         permission_role_edit,
    #         permission_role_delete,
    #         permission_permission_list,
    #         permission_role_permission_create,
    #         permission_role_permission_list
    #     )
    #
    #     perm_list = [
    #         permission_role_create,
    #         permission_role_list,
    #         permission_role_view,
    #         permission_role_edit,
    #         permission_role_delete,
    #         permission_permission_list,
    #         permission_role_permission_create,
    #         permission_role_permission_list
    #     ]
    #
    #     try:
    #         create_permission(perm_list)
    #     except (OperationalError, ProgrammingError):
    #         # It's likely that we're in the middle of an initial migration or similar. Skip for now.
    #         pass
