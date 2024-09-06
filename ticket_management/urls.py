from django.urls import path

from . import views

urlpatterns = [

    # SLA URL
    path('v1/sla', views.SLACreateApi.as_view(), name='sla_create'),
    path('v1/sla/list', views.SLAFilterApi.as_view(), name='sla_list'),
    path('v1/sla/<str:pk>', views.SLARetrieveUpdateDelete.as_view(), name='sla_update'),

]
# Ticket Type URL (tested api level 2 - written Unit test case)
# path('v1/type', views.TicketTypeCreateAPI.as_view(), name='ticket_type_create'),
# path('v1/type/<str:pk>', views.TicketTypeUpdateAPI.as_view(), name='ticket_type_update'),
# path('v1/type/list', views.TicketTypeFilterApi.as_view(), name='ticket_type_list'),


# # Projects URL (tested api level 2 - written Unit test case)
# path('v1/project', views.ProjectCreateApi.as_view(), name='project_create'),
# path('v1/project/list', views.ProjectFilterApi.as_view(), name='project_list_filter'),
# path('v1/project/<int:pk>', views.ProjectRetrieveUpdateDeleteApi.as_view(),
#      name='project_retrieve_update_destroy'),
#
# # Ticket URLs  (tested api level 2 - written Unit test case)
# path('v1', views.TicketCreateAPI.as_view(), name='ticket_create'),
# path('v1/list', views.TicketFilterAPI.as_view(), name='ticket_filter'),
# path('v1/<int:pk>', views.TicketUpdateAPI.as_view(), name='ticket_detail'),
#
# # TicketBehalf URLs (tested api level 2)
# path('v1/behalf', views.TicketBehalfCreateAPI.as_view(), name='ticket_behalf_create'),
# path('v1/behalf/list', views.TicketBehalfFilterAPI.as_view(), name='ticket_behalf_filter'),
# path('v1/behalf/<int:pk>', views.TicketBehalfUpdateAPI.as_view(), name='ticket_behalf_details'),
#
# # TicketFollower URLs (tested api level 2)
# path('v1/follower', views.TicketFollowerCreateAPI.as_view(), name='ticket_follower_create'),
# path('v1/follower/list', views.TicketFollowerFilterAPI.as_view(), name='ticket_follower_filter'),
# path('v1/follower/<int:pk>', views.TicketFollowerUpdateAPI.as_view(), name='ticket_follower_detail'),
#
# # TicketRevision URLs (tested api level 2)
# path('v1/revision', views.TicketRevisionCreateAPI.as_view(), name='ticket_revision_create'),
# path('v1/revision/list', views.TicketRevisionFilterAPI.as_view(), name='ticket_revision_filter'),
# path('v1/revision/<int:pk>', views.TicketRevisionUpdateAPI.as_view(), name='ticket_revision_detail'),
#
# # Priority URLs (tested api level 2 - written Unit test case)
# path('v1/priority', views.PriorityListCreateApi.as_view(), name='priority_list_create'),
# path('v1/priority/<int:pk>', views.PriorityModifyApi.as_view(), name='priority_detail_update_delete'),
