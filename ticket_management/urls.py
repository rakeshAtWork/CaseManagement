from django.urls import path

from . import views

urlpatterns = [
    # Ticket Type URL (tested api level 2 - written Unit test case)
    path('v1/type', views.TicketTypeCreateAPI.as_view(), name='ticket-create'),
    path('v1/type/<str:pk>', views.TicketTypeUpdateAPI.as_view(), name='ticket-update'),
    path('v1/type/list/filter', views.TicketTypeFilterApi.as_view(), name='ticket_type_list'),

    # SLA URL
    path('v1/sla', views.SLACreate.as_view(), name='sla_create'),
    path('v1/sla/list/filter', views.SLAFilterApi.as_view(), name='sla_list'),
    path('v1/sla/<str:pk>', views.SLARetrieveUpdateDelete.as_view(), name='sla_update'),

    # Department URL (tested api level 2 - written Unit test case)
    path('v1/department/list/filter', views.DepartmentFilterApi.as_view(), name='department_list'),
    path('v1/department', views.DepartmentCreateApi.as_view(), name='department_create'),
    path('v1/department/<int:pk>', views.DepartmentUpdateApi.as_view(), name='department_update'),

    # User Department URL (tested api level 2 - written Unit test case)
    path('v1/department/user', views.UserDepartmentApi.as_view(), name='department_user'),

    # Status URL (tested api level 2 - written Unit test case)
    path('v1/status/list/filter', views.StatusFilterApi.as_view(), name='status_list'),
    path('v1/status', views.StatusCreateApi.as_view(), name='status_create'),
    path('v1/status/<int:pk>', views.StatusUpdateApi.as_view(), name='status_update'),

    # Category URL (tested api level 2 -  written Unit test case)
    path('v1/category/list/filter', views.CategoryFilterApi.as_view(), name='category_list'),
    path('v1/category', views.CategoryCreateApi.as_view(), name='category_create'),
    path('v1/category/<int:pk>', views.CategoryUpdateApi.as_view(), name='category_update'),

    # Projects URL (tested api level 2 - written Unit test case)
    path('v1/project', views.ProjectCreateApi.as_view(), name='project_create'),
    path('v1/project/list/filter', views.ProjectFilterApi.as_view(), name='project_list_filter'),
    path('v1/project/<int:pk>', views.ProjectRetrieveUpdateDeleteApi.as_view(),
         name='project_retrieve_update_destroy'),

    # Ticket URLs  (tested api level 2 - written Unit test case)
    path('v1', views.TicketCreateAPI.as_view(), name='ticket_create'),
    path('v1/list/filter', views.TicketFilterAPI.as_view(), name='ticket_filter'),
    path('v1/<int:pk>', views.TicketUpdateAPI.as_view(), name='ticket_detail'),

    # TicketBehalf URLs (tested api level 2)
    path('v1/behalf', views.TicketBehalfCreateAPI.as_view(), name='ticket_behalf_create'),
    path('v1/behalf/list/filter', views.TicketBehalfFilterAPI.as_view(), name='ticket_behalf_filter'),
    path('v1/behalf/<int:pk>', views.TicketBehalfUpdateAPI.as_view(), name='ticket_behalf_details'),

    # TicketFollower URLs (tested api level 2)
    path('v1/follower', views.TicketFollowerCreateAPI.as_view(), name='ticket_follower_create'),
    path('v1/follower/list/filter', views.TicketFollowerFilterAPI.as_view(), name='ticket_follower_filter'),
    path('v1/follower/<int:pk>', views.TicketFollowerUpdateAPI.as_view(), name='ticket_follower_detail'),

    # TicketRevision URLs (tested api level 2)
    path('v1/revision', views.TicketRevisionCreateAPI.as_view(), name='ticket_revision_create'),
    path('v1/revision/list/filter', views.TicketRevisionFilterAPI.as_view(), name='ticket_revision_filter'),
    path('v1/revision/<int:pk>', views.TicketRevisionUpdateAPI.as_view(), name='ticket_revision_detail'),

    # Priority URLs (tested api level 2 - written Unit test case)
    path('v1/priority', views.PriorityListCreateApi.as_view(), name='priority_list_create'),
    path('v1/priority/<int:pk>', views.PriorityModifyApi.as_view(), name='priority_detail_update_delete'),
]
