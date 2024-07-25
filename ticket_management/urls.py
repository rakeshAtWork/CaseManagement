from django.urls import path

from . import views
urlpatterns = [
    path('v1/api/tickettype', views.TicketTypeCreateAPI.as_view(), name='ticket-create'),
    path('v1/api/tickettype/<str:pk>', views.TicketTypeUpdateAPI.as_view(), name='ticket-update'),

    path('v1/api/sla', views.SLACreate.as_view(), name='sla-create'),
    path('v1/api/sla/<str:pk>', views.SLARetrieveUpdateDelete.as_view(), name='sla-update'),

    path('department/list', views.DepartmentFilterApi.as_view(), name='department_list'),
    path('department', views.DepartmentCreateApi.as_view(), name='department_create'),
    path('department/<int:pk>', views.DepartmentUpdateApi.as_view(), name='department_update'),

    path('v1/status/list', views.StatusFilterApi.as_view(), name='status_list'),
    path('v1/status', views.StatusCreateApi.as_view(), name='status_create'),
    path('v1/status/<int:pk>', views.StatusUpdateApi.as_view(), name='status_update'),

    path('v1/category/list', views.CategoryFilterApi.as_view(), name='category_list'),
    path('v1/category', views.CategoryCreateApi.as_view(), name='category_create'),
    path('v1/category/<int:pk>', views.CategoryUpdateApi.as_view(), name='category_update'),

    path('v1/project/create', views.ProjectCreateApi.as_view(), name='project_create'),
    path('v1/project/list/filter', views.ProjectFilterApi.as_view(), name='project_list_filter'),
    path('v1/project/modify/<int:pk>', views.ProjectRetrieveUpdateDeleteApi.as_view(),
         name='project_retrieve_update_destroy'),
]
