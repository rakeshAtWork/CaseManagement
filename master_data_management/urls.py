from django.urls import path

from . import views

urlpatterns = [
    # Unit tests cases written for 3 api end points
    path('v1/file-type', views.FileTypeApi.as_view(), name='file_type'),  # Create new file meta data in db.
    path('v1/file-type/<str:pk>', views.FileTypeModifyApi.as_view(), name='file_type_modify'),
    # This is for Modify and Delete api endpoint.
    path('v1/file-type/list', views.FileTypeFilterApi.as_view(), name='file_type_filter'),
    # getting the file type details based on the pagination and filteration

    path('v1/client', views.ClientApi.as_view(), name='client'),
    path('v1/client/<str:pk>', views.ClientModifyApi.as_view(),
         name='client_modify'),
    path('v1/client/list', views.ClientFilterApi.as_view(),
         name='client_filter'),

    path('v1/customer', views.CustomerApi.as_view(), name='customer'),
    path('v1/customer/<str:pk>', views.CustomerModifyApi.as_view(),
         name='customer_modify'),
    path('v1/customer/list', views.CustomerFilterApi.as_view(),
         name='customer_filter'),

    path('v1/business-unit', views.BusinessUnitApi.as_view(), name='business_unit'),
    path('v1/business-unit/<str:pk>', views.BusinessUnitModifyApi.as_view(),
         name='business_unit_modify'),
    path('v1/business-unit/list', views.BusinessUnitFilterApi.as_view(), name='business_unit_filter'),

    path('v1/vendor', views.VendorApi.as_view(), name='vendor'),
    path('v1/vendor/<str:pk>', views.VendorModifyApi.as_view(),
         name='vendor_modify'),
    path('v1/vendor/list', views.VendorFilterApi.as_view(), name='vendor_filter'),

    # UNit tests cases written for the 3 api endpoint
    path('v1/application', views.ApplicationApi.as_view(), name='application'),
    path('v1/application/<str:pk>', views.ApplicationModifyApi.as_view(),
         name='application_modify'),
    path('v1/application/list', views.ApplicationFilterApi.as_view(), name='application_filter'),

    # added new URL's

    # VendorDetails URLs
    path('v1/vendor', views.VendorDetailsCreateView.as_view(), name='vendor_details_create'),
    path('v1/vendor/<int:pk>', views.VendorDetailsRetrieveUpdateDestroyView.as_view(),
         name='vendor_details_detail'),
    path('v1/vendor/list', views.VendorDetailsFilterApi.as_view(), name='vendor_details_filter'),

    # AccountType URLs
    path('v1/account-type', views.AccountTypeListApi.as_view(), name='account_type_list'),
    path('v1/account-type/<int:pk>', views.AccountTypeModifyApi.as_view(), name='account_type_modify'),

    # SupplierContactDetails URLs
    path('v1/supplier-contact-details', views.SupplierContactDetailsListApi.as_view(),
         name='supplier_contact_details_list_only'),
    path('v1/supplier-contact-details/list', views.SupplierContactDetailsFilterApi.as_view(),
         name='supplier_contact_details_list'),
    path('v1/supplier-contact-details/<int:pk>', views.SupplierContactDetailsModifyApi.as_view(),
         name='supplier_contact_details_modify'),

    # D365FOSetup URLs
    path('v1/d365fo-setup', views.D365FOSetupListApi.as_view(), name='d365fo_setup_list_only'),
    path('v1/d365fo-setup/list', views.D365FOSetupFilterApi.as_view(), name='d365fo_setup_list'),
    path('v1/d365fo-setup/<int:pk>', views.D365FOSetupModifyApi.as_view(), name='d365fo_setup_modify'),

    # CompanyInfoForValidation URLs
    path('v1/company-info-for-validation', views.CompanyInfoForValidationListApi.as_view(),
         name='company_info_for_validation_list'),
    path('v1/company-info-for-validation/<int:pk>', views.CompanyInfoForValidationModifyApi.as_view(),
         name='company_info_for_validation_modify'),

    # CPPSanctionAssessment URLs
    path('v1/cpp-sanction-assessment', views.CPPSanctionAssessmentListApi.as_view(),
         name='cpp_sanction_assessment_list'),
    path('v1/cpp-sanction-assessment/<int:pk>', views.CPPSanctionAssessmentModifyApi.as_view(),
         name='cpp_sanction_assessment_modify'),

    # Country URL (tested api level 2 - written Unit test case)
    path('v1/country/list', views.CountryFilterApi.as_view(), name='country_filter'),
    path('v1/country', views.CountryCreateApi.as_view(), name='country_create'),
    path('v1/country/<int:pk>', views.CountryModifyApi.as_view(), name='country_detail'),

    # Currency URL (tested api level 2 - written Unit test case)
    path('v1/currency/list', views.CurrencyFilterApi.as_view(), name='currency_filter'),
    path('v1/currency', views.CurrencyCreateApi.as_view(), name='currency_create'),
    path('v1/currency/<int:pk>', views.CurrencyModifyApi.as_view(), name='currency_detail'),

    # Department Type (Category) URL (tested api level 2 -  written Unit test case)
    path('v1/category/list', views.CategoryFilterApi.as_view(), name='category_list'),
    path('v1/category', views.CategoryCreateApi.as_view(), name='category_create'),
    path('v1/category/<int:pk>', views.CategoryUpdateApi.as_view(), name='category_update'),

    # Department URL (tested api level 2 - written Unit test case)
    path('v1/department/list', views.DepartmentFilterApi.as_view(), name='department_list'),
    path('v1/department', views.DepartmentCreateApi.as_view(), name='department_create'),
    path('v1/department/<int:pk>', views.DepartmentUpdateApi.as_view(), name='department_update'),

    # User Department URL (tested api level 2 - written Unit test case)
    path('v1/department/user', views.UserDepartmentApi.as_view(), name='department_user'),

    # Status URL (tested api level 2 - written Unit test case)
    path('v1/status/list', views.StatusFilterApi.as_view(), name='status_list'),
    path('v1/status', views.StatusCreateApi.as_view(), name='status_create'),
    path('v1/status/<int:pk>', views.StatusUpdateApi.as_view(), name='status_update'),

    # Email Template Type URL
    path('v1/email-template-types', views.EmailTemplateTypeListCreateView.as_view(),
         name='email_template_type_list_create'),
    path('v1/email-template-types/<int:pk>', views.EmailTemplateTypeRetrieveUpdateDestroyView.as_view(),
         name='email_template_type_detail'),

    # Email Template URL(tested api level 2 - written Unit test case)
    path('v1/email-templates', views.EmailTemplateListCreateApi.as_view(), name='email_template_list_create'),
    path('v1/email-templates/<int:pk>', views.EmailTemplateRetrieveUpdateDestroyApi.as_view(),
         name='email_template_detail'),
    path('v1/email-templates/list', views.EmailTemplateFilterApi.as_view(), name='email_template_list_filter'),

    # User Status URL
    path('v1/user-status', views.UserStatusListCreate.as_view(), name='user_status_list_create'),
    path('v1/user-status/<int:pk>', views.UserStatusDetail.as_view(), name='user_status_detail'),

    # Status Field URL
    path('v1/status-fields', views.StatusFieldListCreateAPIView.as_view(), name='status_field_list_create'),
    path('v1/status-fields/<int:pk>', views.StatusFieldDetailAPIView.as_view(), name='status_field_detail'),

    # User Status Field URL(list all the user with status and its associated status fields)
    path('v1/user-status-fields', views.UserStatusFieldListApiView.as_view(), name='user_status_fields_list'),

    path('v1/supplier-contact-details2', views.SupplierContactDetailsCreateView.as_view(),
         name='supplier_contact_details_create'),

    # Activity Log URL
    path('v1/activity-log/list', views.ActivityLogFilterApi.as_view(), name='activity_log_list'),
    path('v1/activity-log', views.ActivityLogCreateApi.as_view(), name='activity_log_create'),
    path('v1/activity-log/<int:pk>', views.ActivityLogUpdateApi.as_view(), name='activity_log_update'),

    # Module ID and name List URL
    path('v1/modules/list', views.ModuleEnumListAPIView.as_view(), name='module-list'),

    # lob URL
    path('v1/lob', views.LineOfBusinessCreateApi.as_view(), name='lob_create'),
    path('v1/lob/<int:pk>', views.LineOfBusinessUpdateApi.as_view(), name='lob_update'),
    path('v1/lob/list', views.LineOfBusinessFilterApi.as_view(), name='lob_list'),
]
