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

    # added new URL's

    # VendorDetails URLs
    path('vendor', views.VendorDetailsCreateView.as_view(), name='vendor-details-create'),
    path('vendor/<int:pk>/', views.VendorDetailsRetrieveUpdateDestroyView.as_view(),
         name='vendor-details-detail'),
    path('vendor/filter/list', views.VendorDetailsFilterApi.as_view(), name='vendor-details-filter'),

    # AccountType URLs
    path('account-type/', views.AccountTypeListApi.as_view(), name='account-type-list'),
    path('account-type/<int:pk>/', views.AccountTypeModifyApi.as_view(), name='account-type-modify'),

    # SupplierContactDetails URLs
    path('v1/supplier_contact_details/list', views.SupplierContactDetailsListApi.as_view(),
         name='supplier_contact_details_list_only'),
    path('v1/supplier_contact_details/list/filter', views.SupplierContactDetailsFilterApi.as_view(),
         name='supplier_contact_details_list'),
    path('v1/supplier_contact_details/<int:pk>', views.SupplierContactDetailsModifyApi.as_view(),
         name='supplier_contact_details_modify'),

    # D365FOSetup URLs
    path('v1/d365fo_setup/list', views.D365FOSetupListApi.as_view(), name='d365fo_setup_list_only'),
    path('v1/d365fo_setup/list/filter', views.D365FOSetupFilterApi.as_view(), name='d365fo_setup_list'),
    path('v1/d365fo_setup/<int:pk>', views.D365FOSetupModifyApi.as_view(), name='d365fo_setup_modify'),

    # CompanyInfoForValidation URLs
    path('company-info-for-validation/', views.CompanyInfoForValidationListApi.as_view(),
         name='company-info-for-validation-list'),
    path('company-info-for-validation/<int:pk>/', views.CompanyInfoForValidationModifyApi.as_view(),
         name='company-info-for-validation-modify'),

    # CPPSanctionAssessment URLs
    path('cpp-sanction-assessment/', views.CPPSanctionAssessmentListApi.as_view(), name='cpp-sanction-assessment-list'),
    path('cpp-sanction-assessment/<int:pk>/', views.CPPSanctionAssessmentModifyApi.as_view(),
         name='cpp-sanction-assessment-modify'),

]
