from django.urls import path
from . import views

urlpatterns = [
    path('v1/role/list', views.RoleFilterApi.as_view(), name='role_list'),
    # This is list out all the roles(unit test case written - included data check)
    path('v1/role', views.RoleCreateApi.as_view(), name='role_create'),
    # crea a new role with a list of privileges(unit test case written - included data check)
    path('v1/role/<str:pk>', views.RoleUpdateApi.as_view(), name='role_update'),
    # update and delete a role also you can get one role by providing the UUID of the role.(unit test case written)
    path('v1/roles/privileges', views.RoleDetailView.as_view(), name='role_list_privileges'),
    # this is to list all roles with the associated privileges.(unit test case written)
    path('v1/roles/privileges/<str:pk>', views.RoleDetailView.as_view(), name='role_detail_privileges'),
    # this is to list a specific role with the associated privileges.(unit test case written )

    path('v1/role/user', views.RoleUserCreateAPI.as_view(), name='role_user_create'),
    # this is for to assign a role to a list of User.(unit test case written)

    path('v1/privilege/list', views.PermissionFilterApi.as_view(), name='privilege_list'),
    # this is to list out all the privileges(unit test case written - included data check)
    path('v1/privilege-populate', views.PopulatePermissionsView.as_view(), name="populate_privileges"),
    # this is to populate newly created privileges in to MasterPrivileges Models.

    path('v1/configurations', views.AppConfigurationListCreateAPIView.as_view(), name='appconfiguration_list_create'),
    # this is for app configuration creation and list end point (Unit test case written - included data check)
    path('v1/configurations/<int:pk>', views.AppConfigurationRetrieveUpdateDestroyAPIView.as_view(),
         name='appconfiguration_detail'),
    # This is for app configuration update api end point(unit test case written - included data check)

    path('v1/client/privilege/list', views.ClientPrivilegeFilterApi.as_view(), name='client_privilege_filter'),
    path('v1/client/privilege', views.ClientPrivilegeApi.as_view(), name='client_privilege'),
    path('v1/client/privilege/<str:pk>', views.ClientPrivilegeModifyApi.as_view(), name='client_privilege_update'),

]
