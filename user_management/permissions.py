from django.utils.translation import gettext_lazy as _

from acl.classes import PermissionNamespace

namespace = PermissionNamespace("User Permissions")

permission_user_list_view = namespace.add_permission(
    privilege_desc=_('All Users list viewed!'), privilege_name='VIEW_USER_LIST', module_id=50
)
permission_user_create = namespace.add_permission(
    privilege_desc=_('New User created with required permissions!'), privilege_name='CREATE_USER',
    module_id=50
)
permission_user_detail_view = namespace.add_permission(
    privilege_desc=_('Specific User details viewed!'), privilege_name='GET_SINGLE_USER_DETAILS', module_id=50
)
permission_user_detail_edit = namespace.add_permission(
    privilege_desc=_('Specific User details updated!'), privilege_name='UPDATE_USER', module_id=50
)
permission_user_detail_delete = namespace.add_permission(
    privilege_desc=_('Specific User deleted!'), privilege_name='DELETE_USER', module_id=50
)
permission_user_short_info = namespace.add_permission(
    privilege_desc=_('Specific User short info viewed!'), privilege_name='VIEW_USER_SHORT_INFO_LIST', module_id=50
)
permission_profile_details = namespace.add_permission(
    privilege_desc=_('User profile details viewed!'), privilege_name='GET_USER_PROFILE', module_id=50
)
permission_profile_update = namespace.add_permission(
    privilege_desc=_('User profile details updated!'), privilege_name='UPDATE_USER_PROFILE', module_id=50
)
permission_logout_user = namespace.add_permission(
    privilege_desc=_('User logged out from the application!'), privilege_name='LOGOUT_USER',
    module_id=50
)
