from django.utils.translation import gettext_lazy as _

from acl.classes import PermissionNamespace

namespace = PermissionNamespace("MDM Permissions")

# #file_type_management
# permission_file_type_create = namespace.add_permission(
#     privilege_desc=_('New Document field created successfully!'), privilege_name='CREATE_FILE_TYPE',
#     module_id=10
# )
# permission_file_type_list = namespace.add_permission(
#     privilege_desc=_('View all Document field'), privilege_name='VIEW_FILE_TYPE_LIST', module_id=10
# )
# permission_file_type_view = namespace.add_permission(
#     privilege_desc=_('Viewed a specific Document field!'), privilege_name='VIEW_FILE_TYPE', module_id=10
# )
# permission_file_type_edit = namespace.add_permission(
#     privilege_desc=_('Document field is updated!'), privilege_name='UPDATE_FILE_TYPE',
#     module_id=10
# )
# permission_file_type_delete = namespace.add_permission(
#     privilege_desc=_('Document field is deleted!'), privilege_name='DELETE_FILE_TYPE', module_id=10
# )
# customer_management
# permission_customer_create = namespace.add_permission(
#     privilege_desc=_('New Customer created successfully!'), privilege_name='CREATE_CUSTOMER',
#     module_id=240
# )
# permission_customer_list = namespace.add_permission(
#     privilege_desc=_('View all Customer'), privilege_name='VIEW_CUSTOMER_LIST', module_id=240
# )
# permission_customer_view = namespace.add_permission(
#     privilege_desc=_('Viewed a specific Customer!'), privilege_name='VIEW_CUSTOMER', module_id=240
# )
# permission_customer_edit = namespace.add_permission(
#     privilege_desc=_('Customer is updated!'), privilege_name='UPDATE_CUSTOMER',
#     module_id=240
# )
# permission_customer_delete = namespace.add_permission(
#     privilege_desc=_('Customer is deleted!'), privilege_name='DELETE_CUSTOMER', module_id=240
# )
# permission_client_create = namespace.add_permission(
#     privilege_desc=_('New Client created successfully!'), privilege_name='CREATE_CLIENT',
#     module_id=240
# )
# permission_client_list = namespace.add_permission(
#     privilege_desc=_('View all Client'), privilege_name='VIEW_CLIENT_LIST', module_id=240
# )
# permission_client_view = namespace.add_permission(
#     privilege_desc=_('Viewed a specific Client!'), privilege_name='VIEW_CLIENT', module_id=240
# )
# permission_client_edit = namespace.add_permission(
#     privilege_desc=_('Client is updated!'), privilege_name='UPDATE_CLIENT',
#     module_id=240
# )
# permission_client_delete = namespace.add_permission(
#     privilege_desc=_('Client is deleted!'), privilege_name='DELETE_CLIENT', module_id=240
# )
# #business_unit_management
# permission_business_unit_create = namespace.add_permission(
#     privilege_desc=_('New Business unit created successfully!'), privilege_name='CREATE_BUSINESS_UNIT',
#     module_id=40
# )
# permission_business_unit_list = namespace.add_permission(
#     privilege_desc=_('View all Business unit'), privilege_name='VIEW_BUSINESS_UNIT_LIST', module_id=40
# )
# permission_business_unit_view = namespace.add_permission(
#     privilege_desc=_('Viewed a specific Business unit!'), privilege_name='VIEW_BUSINESS_UNIT', module_id=40
# )
# permission_business_unit_edit = namespace.add_permission(
#     privilege_desc=_('Business unit is updated!'), privilege_name='UPDATE_BUSINESS_UNIT',
#     module_id=40
# )
# permission_business_unit_delete = namespace.add_permission(
#     privilege_desc=_('Business unit is deleted!'), privilege_name='DELETE_BUSINESS_UNIT', module_id=40
# )

# #vendor_management
# permission_vendor_create = namespace.add_permission(
#     privilege_desc=_('New Vendor created successfully!'), privilege_name='CREATE_VENDOR',
#     module_id=30
# )
# permission_vendor_list = namespace.add_permission(
#     privilege_desc=_('View all Vendor'), privilege_name='VIEW_VENDOR_LIST', module_id=30
# )
# permission_vendor_view = namespace.add_permission(
#     privilege_desc=_('Viewed a specific Vendor!'), privilege_name='VIEW_VENDOR', module_id=30
# )
# permission_vendor_edit = namespace.add_permission(
#     privilege_desc=_('Vendor is updated!'), privilege_name='UPDATE_VENDOR',
#     module_id=30
# )
# permission_vendor_delete = namespace.add_permission(
#     privilege_desc=_('Vendor is deleted!'), privilege_name='DELETE_VENDOR', module_id=30
# )
# #application_management
# permission_application_create = namespace.add_permission(
#     privilege_desc=_('New Application created successfully!'), privilege_name='CREATE_APPLICATION',
#     module_id=50
# )
# permission_application_list = namespace.add_permission(
#     privilege_desc=_('View all Application'), privilege_name='VIEW_APPLICATION_LIST', module_id=50
# )
# permission_application_view = namespace.add_permission(
#     privilege_desc=_('Viewed a specific Application!'), privilege_name='VIEW_APPLICATION', module_id=50
# )
# permission_application_edit = namespace.add_permission(
#     privilege_desc=_('Application is updated!'), privilege_name='UPDATE_APPLICATION',
#     module_id=50
# )
# permission_application_delete = namespace.add_permission(
#     privilege_desc=_('Application is deleted!'), privilege_name='DELETE_APPLICATION', module_id=50
# )

# Country Management
permission_country_create = namespace.add_permission(
    privilege_desc=_('New Country created successfully!'), privilege_name='CREATE_COUNTRY',
    module_id=300
)

permission_country_list = namespace.add_permission(
    privilege_desc=_('View all Countries'), privilege_name='VIEW_COUNTRY_LIST', module_id=300
)

permission_country_view = namespace.add_permission(
    privilege_desc=_('Viewed a specific Country!'), privilege_name='VIEW_COUNTRY', module_id=300
)

permission_country_edit = namespace.add_permission(
    privilege_desc=_('Country is updated!'), privilege_name='UPDATE_COUNTRY',
    module_id=300
)

permission_country_delete = namespace.add_permission(
    privilege_desc=_('Country is deleted!'), privilege_name='DELETE_COUNTRY', module_id=300
)

# Currency Management
permission_currency_create = namespace.add_permission(
    privilege_desc=_('New Currency created successfully!'), privilege_name='CREATE_CURRENCY',
    module_id=260
)

permission_currency_list = namespace.add_permission(
    privilege_desc=_('View all Currencies'), privilege_name='VIEW_CURRENCY_LIST', module_id=260
)

permission_currency_view = namespace.add_permission(
    privilege_desc=_('Viewed a specific Currency!'), privilege_name='VIEW_CURRENCY', module_id=260
)

permission_currency_edit = namespace.add_permission(
    privilege_desc=_('Currency is updated!'), privilege_name='UPDATE_CURRENCY',
    module_id=260
)

permission_currency_delete = namespace.add_permission(
    privilege_desc=_('Currency is deleted!'), privilege_name='DELETE_CURRENCY', module_id=260
)
# Category Management
permission_category_create = namespace.add_permission(
    privilege_desc=_('New Category created successfully!'), privilege_name='CREATE_CATEGORY',
    module_id=160
)

permission_category_list = namespace.add_permission(
    privilege_desc=_('View all Categories'), privilege_name='VIEW_CATEGORY_LIST', module_id=160
)

permission_category_view = namespace.add_permission(
    privilege_desc=_('Viewed a specific Category!'), privilege_name='VIEW_CATEGORY', module_id=160
)

permission_category_edit = namespace.add_permission(
    privilege_desc=_('Category is updated!'), privilege_name='UPDATE_CATEGORY',
    module_id=160
)

permission_category_delete = namespace.add_permission(
    privilege_desc=_('Category is deleted!'), privilege_name='DELETE_CATEGORY', module_id=160
)
# Department Management
permission_department_create = namespace.add_permission(
    privilege_desc=_('New Department created successfully!'), privilege_name='CREATE_DEPARTMENT',
    module_id=160
)

permission_department_list = namespace.add_permission(
    privilege_desc=_('View all Departments'), privilege_name='VIEW_DEPARTMENT_LIST', module_id=160
)

permission_department_view = namespace.add_permission(
    privilege_desc=_('Viewed a specific Department!'), privilege_name='VIEW_DEPARTMENT', module_id=160
)

permission_department_edit = namespace.add_permission(
    privilege_desc=_('Department is updated!'), privilege_name='UPDATE_DEPARTMENT',
    module_id=160
)

permission_department_delete = namespace.add_permission(
    privilege_desc=_('Department is deleted!'), privilege_name='DELETE_DEPARTMENT', module_id=160
)
# Status Management
permission_status_create = namespace.add_permission(
    privilege_desc=_('New Status created successfully!'), privilege_name='CREATE_STATUS',
    module_id=280  # Use the appropriate module ID
)

permission_status_list = namespace.add_permission(
    privilege_desc=_('View all Statuses'), privilege_name='VIEW_STATUS_LIST', module_id=280
)

permission_status_view = namespace.add_permission(
    privilege_desc=_('Viewed a specific Status!'), privilege_name='VIEW_STATUS', module_id=280
)

permission_status_edit = namespace.add_permission(
    privilege_desc=_('Status is updated!'), privilege_name='UPDATE_STATUS',
    module_id=280
)

permission_status_delete = namespace.add_permission(
    privilege_desc=_('Status is deleted!'), privilege_name='DELETE_STATUS', module_id=280
)
# Email Template Management
permission_email_template_create = namespace.add_permission(
    privilege_desc=_('New Email Template created successfully!'), privilege_name='CREATE_EMAIL_TEMPLATE',
    module_id=270
)

permission_email_template_list = namespace.add_permission(
    privilege_desc=_('View all Email Templates'), privilege_name='VIEW_EMAIL_TEMPLATE_LIST', module_id=270
)

permission_email_template_view = namespace.add_permission(
    privilege_desc=_('Viewed a specific Email Template!'), privilege_name='VIEW_EMAIL_TEMPLATE', module_id=270
)

permission_email_template_edit = namespace.add_permission(
    privilege_desc=_('Email Template is updated!'), privilege_name='UPDATE_EMAIL_TEMPLATE',
    module_id=270
)

permission_email_template_delete = namespace.add_permission(
    privilege_desc=_('Email Template is deleted!'), privilege_name='DELETE_EMAIL_TEMPLATE', module_id=270
)
# User Status Management
permission_user_status_create = namespace.add_permission(
    privilege_desc=_('New User Status created successfully!'), privilege_name='CREATE_USER_STATUS',
    module_id=7  # Use the appropriate module ID
)

permission_user_status_list = namespace.add_permission(
    privilege_desc=_('View all User Statuses'), privilege_name='VIEW_USER_STATUS_LIST', module_id=7
)

permission_user_status_view = namespace.add_permission(
    privilege_desc=_('Viewed a specific User Status!'), privilege_name='VIEW_USER_STATUS', module_id=7
)

permission_user_status_edit = namespace.add_permission(
    privilege_desc=_('User Status is updated!'), privilege_name='UPDATE_USER_STATUS',
    module_id=7
)

permission_user_status_delete = namespace.add_permission(
    privilege_desc=_('User Status is deleted!'), privilege_name='DELETE_USER_STATUS', module_id=7
)
# Status Field Management
permission_status_field_create = namespace.add_permission(
    privilege_desc=_('New Status Field created successfully!'), privilege_name='CREATE_STATUS_FIELD',
    module_id=8  # Use the appropriate module ID
)

permission_status_field_list = namespace.add_permission(
    privilege_desc=_('View all Status Fields'), privilege_name='VIEW_STATUS_FIELD_LIST', module_id=8
)

permission_status_field_view = namespace.add_permission(
    privilege_desc=_('Viewed a specific Status Field!'), privilege_name='VIEW_STATUS_FIELD', module_id=8
)

permission_status_field_edit = namespace.add_permission(
    privilege_desc=_('Status Field is updated!'), privilege_name='UPDATE_STATUS_FIELD',
    module_id=8
)

permission_status_field_delete = namespace.add_permission(
    privilege_desc=_('Status Field is deleted!'), privilege_name='DELETE_STATUS_FIELD', module_id=8
)
# User Status Field Management
permission_user_status_field_list = namespace.add_permission(
    privilege_desc=_('View all User Status Fields'), privilege_name='VIEW_USER_STATUS_FIELD_LIST',
    module_id=9
)
# Line Of Business
permission_line_of_business_create = namespace.add_permission(
    privilege_desc=_('New Line Of Business created successfully!'),
    privilege_name='CREATE_LINE_OF_BUSINESS',
    module_id=310
)

permission_line_of_business_list = namespace.add_permission(
    privilege_desc=_('View all Line Of Business'),
    privilege_name='VIEW_LINE_OF_BUSINESS_LIST',
    module_id=310
)

permission_line_of_business_view = namespace.add_permission(
    privilege_desc=_('Viewed a specific Line Of Business!'),
    privilege_name='VIEW_LINE_OF_BUSINESS',
    module_id=310
)

permission_line_of_business_edit = namespace.add_permission(
    privilege_desc=_('Line Of Business is updated!'),
    privilege_name='UPDATE_LINE_OF_BUSINESS',
    module_id=310
)

permission_line_of_business_delete = namespace.add_permission(
    privilege_desc=_('Line Of Business is deleted!'),
    privilege_name='DELETE_LINE_OF_BUSINESS',
    module_id=310
)
# Legal Entity
permission_legal_entity_create = namespace.add_permission(
    privilege_desc=_('New Legal Entity created successfully!'),
    privilege_name='CREATE_LEGAL_ENTITY',
    module_id=320
)

permission_legal_entity_list = namespace.add_permission(
    privilege_desc=_('View all Legal Entities'),
    privilege_name='VIEW_LEGAL_ENTITY_LIST',
    module_id=320
)

permission_legal_entity_view = namespace.add_permission(
    privilege_desc=_('Viewed a specific Legal Entity!'),
    privilege_name='VIEW_LEGAL_ENTITY',
    module_id=320
)

permission_legal_entity_edit = namespace.add_permission(
    privilege_desc=_('Legal Entity is updated!'),
    privilege_name='UPDATE_LEGAL_ENTITY',
    module_id=320
)

permission_legal_entity_delete = namespace.add_permission(
    privilege_desc=_('Legal Entity is deleted!'),
    privilege_name='DELETE_LEGAL_ENTITY',
    module_id=320
)

# Activity Log
permission_activity_log_list = namespace.add_permission(
    privilege_desc=_('View all Activity Log entries'),
    privilege_name='VIEW_ACTIVITY_LOG_LIST',
    module_id=330
)
