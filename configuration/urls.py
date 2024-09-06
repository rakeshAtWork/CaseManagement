from django.urls import path

from . import views

urlpatterns = [
    path('v1/column-configurations', views.ConfigurationCreateAPIView.as_view(), name='configuration_list_create'),
    path('v1/column-configuration/list', views.ConfigurationListAPIView.as_view(), name='configuration_list'),
    path('v1/column-configurations/modify/<int:pk>', views.ConfigurationRetrieveUpdateDestroyAPIView.as_view(),
         name='configuration_detail'),

]
