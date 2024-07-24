from django.urls import path

from . import views

urlpatterns = [
    path('v1/file/type', views.FileTypeApi.as_view(), name='file_type'),  # Create new file meta data in db.
    path('v1/file/type/<str:pk>', views.FileTypeModifyApi.as_view(), name='file_type_modify'),
    # This is for Modify and Delete api endpoint.
    path('v1/file/type/filter/list', views.FileTypeFilterApi.as_view(), name='file_type_filter'),
    # getting the file type details based on the pagination and filteration

    path('v1/client', views.ClientApi.as_view(), name='client'),
    path('v1/client/<str:pk>', views.ClientModifyApi.as_view(),
         name='client_modify'),
    path('v1/client/filter/list', views.ClientFilterApi.as_view(),
         name='client_filter'),

    path('v1/customer', views.CustomerApi.as_view(), name='customer'),
    path('v1/customer/<str:pk>', views.CustomerModifyApi.as_view(),
         name='customer_modify'),
    path('v1/customer/filter/list', views.CustomerFilterApi.as_view(),
         name='customer_filter'),

    path('v1/business/unit', views.BusinessUnitApi.as_view(), name='business_unit'),
    path('v1/business/unit/<str:pk>', views.BusinessUnitModifyApi.as_view(),
         name='business_unit_modify'),
    path('v1/business/unit/filter/list', views.BusinessUnitFilterApi.as_view(), name='business_unit_filter'),

    path('v1/vendor', views.VendorApi.as_view(), name='vendor'),
    path('v1/vendor/<str:pk>', views.VendorModifyApi.as_view(),
         name='vendor_modify'),
    path('v1/vendor/filter/list', views.VendorFilterApi.as_view(), name='vendor_filter'),

    path('v1/application', views.ApplicationApi.as_view(), name='application'),
    path('v1/application/<str:pk>', views.ApplicationModifyApi.as_view(),
         name='application_modify'),
    path('v1/application/filter/list', views.ApplicationFilterApi.as_view(), name='application_filter'),

]
