from django.utils.translation import gettext_lazy as _

from acl.classes import PermissionNamespace

namespace = PermissionNamespace("MDM Permissions")

permission_file_type_create = namespace.add_permission(
    privilege_desc=_('New Document field created successfully!'), privilege_name='CREATE_FILE_TYPE',
    module_id=100
)
permission_file_type_list = namespace.add_permission(
    privilege_desc=_('View all Document field'), privilege_name='VIEW_FILE_TYPE_LIST', module_id=100
)
permission_file_type_view = namespace.add_permission(
    privilege_desc=_('Viewed a specific Document field!'), privilege_name='VIEW_FILE_TYPE', module_id=100
)
permission_file_type_edit = namespace.add_permission(
    privilege_desc=_('Document field is updated!'), privilege_name='UPDATE_FILE_TYPE',
    module_id=100
)
permission_file_type_delete = namespace.add_permission(
    privilege_desc=_('Document field is deleted!'), privilege_name='DELETE_FILE_TYPE', module_id=100
)
permission_customer_create = namespace.add_permission(
    privilege_desc=_('New Customer created successfully!'), privilege_name='CREATE_CUSTOMER',
    module_id=110
)
permission_customer_list = namespace.add_permission(
    privilege_desc=_('View all Customer'), privilege_name='VIEW_CUSTOMER_LIST', module_id=110
)
permission_customer_view = namespace.add_permission(
    privilege_desc=_('Viewed a specific Customer!'), privilege_name='VIEW_CUSTOMER', module_id=110
)
permission_customer_edit = namespace.add_permission(
    privilege_desc=_('Customer is updated!'), privilege_name='UPDATE_CUSTOMER',
    module_id=110
)
permission_customer_delete = namespace.add_permission(
    privilege_desc=_('Customer is deleted!'), privilege_name='DELETE_CUSTOMER', module_id=110
)
permission_client_create = namespace.add_permission(
    privilege_desc=_('New Client created successfully!'), privilege_name='CREATE_CLIENT',
    module_id=110
)
permission_client_list = namespace.add_permission(
    privilege_desc=_('View all Client'), privilege_name='VIEW_CLIENT_LIST', module_id=110
)
permission_client_view = namespace.add_permission(
    privilege_desc=_('Viewed a specific Client!'), privilege_name='VIEW_CLIENT', module_id=110
)
permission_client_edit = namespace.add_permission(
    privilege_desc=_('Client is updated!'), privilege_name='UPDATE_CLIENT',
    module_id=110
)
permission_client_delete = namespace.add_permission(
    privilege_desc=_('Client is deleted!'), privilege_name='DELETE_CLIENT', module_id=110
)
permission_business_unit_create = namespace.add_permission(
    privilege_desc=_('New Business unit created successfully!'), privilege_name='CREATE_BUSINESS_UNIT',
    module_id=120
)
permission_business_unit_list = namespace.add_permission(
    privilege_desc=_('View all Business unit'), privilege_name='VIEW_BUSINESS_UNIT_LIST', module_id=120
)
permission_business_unit_view = namespace.add_permission(
    privilege_desc=_('Viewed a specific Business unit!'), privilege_name='VIEW_BUSINESS_UNIT', module_id=120
)
permission_business_unit_edit = namespace.add_permission(
    privilege_desc=_('Business unit is updated!'), privilege_name='UPDATE_BUSINESS_UNIT',
    module_id=120
)
permission_business_unit_delete = namespace.add_permission(
    privilege_desc=_('Business unit is deleted!'), privilege_name='DELETE_BUSINESS_UNIT', module_id=120
)
permission_vendor_create = namespace.add_permission(
    privilege_desc=_('New Vendor created successfully!'), privilege_name='CREATE_VENDOR',
    module_id=130
)
permission_vendor_list = namespace.add_permission(
    privilege_desc=_('View all Vendor'), privilege_name='VIEW_VENDOR_LIST', module_id=130
)
permission_vendor_view = namespace.add_permission(
    privilege_desc=_('Viewed a specific Vendor!'), privilege_name='VIEW_VENDOR', module_id=130
)
permission_vendor_edit = namespace.add_permission(
    privilege_desc=_('Vendor is updated!'), privilege_name='UPDATE_VENDOR',
    module_id=130
)
permission_vendor_delete = namespace.add_permission(
    privilege_desc=_('Vendor is deleted!'), privilege_name='DELETE_VENDOR', module_id=130
)
permission_application_create = namespace.add_permission(
    privilege_desc=_('New Application created successfully!'), privilege_name='CREATE_APPLICATION',
    module_id=140
)
permission_application_list = namespace.add_permission(
    privilege_desc=_('View all Application'), privilege_name='VIEW_APPLICATION_LIST', module_id=140
)
permission_application_view = namespace.add_permission(
    privilege_desc=_('Viewed a specific Application!'), privilege_name='VIEW_APPLICATION', module_id=140
)
permission_application_edit = namespace.add_permission(
    privilege_desc=_('Application is updated!'), privilege_name='UPDATE_APPLICATION',
    module_id=140
)
permission_application_delete = namespace.add_permission(
    privilege_desc=_('Application is deleted!'), privilege_name='DELETE_APPLICATION', module_id=140
)
