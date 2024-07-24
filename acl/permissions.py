from django.utils.translation import gettext_lazy as _
from .classes import PermissionNamespace

namespace = PermissionNamespace("ACL Permissions")
# role
permission_role_create = namespace.add_permission(
    privilege_desc=_('New Role is created successfully!'), privilege_name='CREATE_ROLE', module_id=10
)
permission_role_list = namespace.add_permission(
    privilege_desc=_('Viewed all Roles!'), privilege_name='VIEW_ROLE_LIST', module_id=10
)
permission_role_view = namespace.add_permission(
    privilege_desc=_('Viewed a specific Role details!'), privilege_name='VIEW_ROLE', module_id=10
)
permission_role_edit = namespace.add_permission(
    privilege_desc=_('Role is updated!'), privilege_name='UPDATE_ROLE',
    module_id=10
)
permission_role_delete = namespace.add_permission(
    privilege_desc=_('Role is deleted!'), privilege_name='DELETE_ROLE', module_id=10
)

# permission
permission_permission_list = namespace.add_permission(
    privilege_desc=_('Viewed all permission list!'), privilege_name='VIEW_PRIVILEGE_LIST',
    module_id=20
)

# role permission
permission_role_permission_create = namespace.add_permission(
    privilege_desc=_('New permission is added successfully to a Role!'), privilege_name='CREATE_ROLE_PERMISSION',
    module_id=30
)
permission_role_permission_list = namespace.add_permission(
    privilege_desc=_('Viewed all permissions list for a specific Role!'), privilege_name='VIEW_ROLE_PERMISSION_LIST',
    module_id=30
)

# client permission
permission_client_permission_create = namespace.add_permission(
    privilege_desc=_('Client added successfully to a specific Permission!'),
    privilege_name='CREATE_CLIENT_PERMISSION',
    module_id=40
)
permission_client_permission_list = namespace.add_permission(
    privilege_desc=_('View all permissions list for all Clients!'),
    privilege_name='VIEW_CLIENT_PERMISSION_LIST', module_id=40
)
permission_client_permission_view = namespace.add_permission(
    privilege_desc=_('View  permissions for a Client!'),
    privilege_name='VIEW_CLIENT_PERMISSION', module_id=40
)
permission_client_permission_edit = namespace.add_permission(
    privilege_desc=_('Client  updated successfully for a specific permission!'),
    privilege_name='UPDATE_CLIENT_PERMISSION', module_id=40
)
permission_client_permission_delete = namespace.add_permission(
    privilege_desc=_('Client deleted successfully for a specific permission!'),
    privilege_name='DELETE_CLIENT_PERMISSION', module_id=40
)

# role user
permission_role_user_create = namespace.add_permission(
    privilege_desc=_('New Role is added successfully to a User!'), privilege_name='CREATE_USER_ROLE',
    module_id=150
)
