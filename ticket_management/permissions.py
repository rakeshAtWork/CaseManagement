from django.utils.translation import gettext_lazy as _

from acl.classes import PermissionNamespace

namespace = PermissionNamespace("Ticket Permissions")

#UserDepartment
permission_user_department_create = namespace.add_permission(
    privilege_desc=_('New User Department!'), privilege_name='CREATE_USER_DEPARTMENT',
    module_id=110
)
permission_user_department_view = namespace.add_permission(
    privilege_desc=_('User Department List!'), privilege_name='VIEW_USER_DEPARTMENT',
    module_id=110
)
permission_user_department_edit = namespace.add_permission(
    privilege_desc=_('User Department Edit!'), privilege_name='EDIT_USER_DEPARTMENT',
    module_id=110
)
permission_user_department_delete = namespace.add_permission(
    privilege_desc=_('Delete Department Edit!'), privilege_name='DELETE_USER_DEPARTMENT',
    module_id=110
)
permission_user_department_view = namespace.add_permission(
    privilege_desc=_('View User Department Edit!'), privilege_name='VIEW_USER_DEPARTMENT',
    module_id=110
)

# TicketType
permission_ticket_type_create = namespace.add_permission(
    privilege_desc=_('Create Ticket Type'), privilege_name='CREATE_TICKET_TYPE',
    module_id=120
)
permission_ticket_type_edit = namespace.add_permission(
    privilege_desc=_('Edit Ticket Type'), privilege_name='EDIT_TICKET_TYPE',
    module_id=120
)
permission_ticket_type_delete = namespace.add_permission(
    privilege_desc=_('Delete Ticket Type'), privilege_name='DELETE_TICKET_TYPE',
    module_id=120
)

# SLA
permission_sla_create = namespace.add_permission(
    privilege_desc=_('Create SLA'), privilege_name='CREATE_SLA',
    module_id=130
)
permission_sla_edit = namespace.add_permission(
    privilege_desc=_('Edit SLA'), privilege_name='EDIT_SLA',
    module_id=130
)
permission_sla_view = namespace.add_permission(
    privilege_desc=_('View SLA'), privilege_name='VIEW_SLA',
    module_id=130
)
permission_sla_delete = namespace.add_permission(
    privilege_desc=_('Delete SLA'), privilege_name='DELETE_SLA',
    module_id=130
)

# Department
permission_department_view = namespace.add_permission(
    privilege_desc=_('View Department'), privilege_name='VIEW_DEPARTMENT',
    module_id=140
)
permission_department_create = namespace.add_permission(
    privilege_desc=_('Create Department'), privilege_name='CREATE_DEPARTMENT',
    module_id=140
)
permission_department_edit = namespace.add_permission(
    privilege_desc=_('Edit Department'), privilege_name='EDIT_DEPARTMENT',
    module_id=140
)
permission_department_delete = namespace.add_permission(
    privilege_desc=_('Delete Department'), privilege_name='DELEET_DEPARTMENT',
    module_id=140
)

# Status
permission_status_view = namespace.add_permission(
    privilege_desc=_('View Status'), privilege_name='VIEW_STATUS',
    module_id=150
)
permission_status_create = namespace.add_permission(
    privilege_desc=_('Create Status'), privilege_name='CREATE_STATUS',
    module_id=150
)
permission_status_edit = namespace.add_permission(
    privilege_desc=_('Edit Status'), privilege_name='EDIT_STATUS',
    module_id=150
)

# Category
permission_category_view = namespace.add_permission(
    privilege_desc=_('View Category'), privilege_name='VIEW_CATEGORY',
    module_id=160
)
permission_category_create = namespace.add_permission(
    privilege_desc=_('Create Category'), privilege_name='CREATE_CATEGORY',
    module_id=160
)
permission_category_edit = namespace.add_permission(
    privilege_desc=_('Edit Category'), privilege_name='EDIT_CATEGORY',
    module_id=160
)
permission_category_delete = namespace.add_permission(
    privilege_desc=_('Delete Category'), privilege_name='DELETE_CATEGORY',
    module_id=160
)

# Projects
permission_project_create = namespace.add_permission(
    privilege_desc=_('Create Project'), privilege_name='CREATE_PROJECT',
    module_id=170
)
permission_project_view = namespace.add_permission(
    privilege_desc=_('View Project'), privilege_name='VIEW_PROJECT',
    module_id=170
)
permission_project_edit = namespace.add_permission(
    privilege_desc=_('Edit Project'), privilege_name='EDIT_PROJECT',
    module_id=170
)
permission_project_delete = namespace.add_permission(
    privilege_desc=_('Delete Project'), privilege_name='DELETE_PROJECT',
    module_id=170
)

# Ticket
permission_ticket_create = namespace.add_permission(
    privilege_desc=_('Create Ticket'), privilege_name='CREATE_TICKET',
    module_id=180
)
permission_ticket_view = namespace.add_permission(
    privilege_desc=_('View Ticket'), privilege_name='VIEW_TICKET',
    module_id=180
)
permission_ticket_edit = namespace.add_permission(
    privilege_desc=_('Edit Ticket'), privilege_name='EDIT_TICKET',
    module_id=180
)
permission_ticket_delete = namespace.add_permission(
    privilege_desc=_('Delete Ticket'), privilege_name='DELETE_TICKET',
    module_id=180
)

# TicketBehalf
permission_ticket_behalf_create = namespace.add_permission(
    privilege_desc=_('Create Ticket Behalf'), privilege_name='CREATE_TICKET_BEHALF',
    module_id=190
)
permission_ticket_behalf_view = namespace.add_permission(
    privilege_desc=_('View Ticket Behalf'), privilege_name='VIEW_TICKET_BEHALF',
    module_id=190
)
permission_ticket_behalf_edit = namespace.add_permission(
    privilege_desc=_('Edit Ticket Behalf'), privilege_name='EDIT_TICKET_BEHALF',
    module_id=190
)
permission_ticket_behalf_delete = namespace.add_permission(
    privilege_desc=_('Delete Ticket Behalf'), privilege_name='DELETE_TICKET_BEHALF',
    module_id=190
)

# TicketFollower
permission_ticket_follower_create = namespace.add_permission(
    privilege_desc=_('Create Ticket Follower'), privilege_name='CREATE_TICKET_FOLLOWER',
    module_id=200
)
permission_ticket_follower_view = namespace.add_permission(
    privilege_desc=_('View Ticket Follower'), privilege_name='VIEW_TICKET_FOLLOWER',
    module_id=200
)
permission_ticket_follower_edit = namespace.add_permission(
    privilege_desc=_('Edit Ticket Follower'), privilege_name='EDIT_TICKET_FOLLOWER',
    module_id=200
)
permission_ticket_follower_delete = namespace.add_permission(
    privilege_desc=_('Delete Ticket Follower'), privilege_name='DELETE_TICKET_FOLLOWER',
    module_id=200
)

# TicketRevision
permission_ticket_revision_create = namespace.add_permission(
    privilege_desc=_('Create Ticket Revision'), privilege_name='CREATE_TICKET_REVISION',
    module_id=210
)
permission_ticket_revision_view = namespace.add_permission(
    privilege_desc=_('View Ticket Revision'), privilege_name='VIEW_TICKET_REVISION',
    module_id=210
)
permission_ticket_revision_edit = namespace.add_permission(
    privilege_desc=_('Edit Ticket Revision'), privilege_name='EDIT_TICKET_REVISION',
    module_id=210
)
permission_ticket_revision_delete = namespace.add_permission(
    privilege_desc=_('Delete Ticket Revision'), privilege_name='DELETE_TICKET_REVISION',
    module_id=210
)

# Priority
permission_priority_create = namespace.add_permission(
    privilege_desc=_('Create Priority'), privilege_name='CREATE_PRIORITY',
    module_id=220
)
permission_priority_view = namespace.add_permission(
    privilege_desc=_('View Priority'), privilege_name='VIEW_PRIORITY',
    module_id=220
)
permission_priority_edit = namespace.add_permission(
    privilege_desc=_('Edit Priority'), privilege_name='EDIT_PRIORITY',
    module_id=220
)
permission_priority_delete = namespace.add_permission(
    privilege_desc=_('Delete Priority'), privilege_name='DELETE_PRIORITY',
    module_id=220
)