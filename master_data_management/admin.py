from django.contrib import admin
from .models import VendorDetails, AccountType, \
    SupplierContactDetails, D365FOSetup, CompanyInfoForValidation, CPPSanctionAssessment, Status, StatusField, \
    UserStatus, ActivityLog

admin.site.register(SupplierContactDetails)
admin.site.register(D365FOSetup)
admin.site.register(CompanyInfoForValidation)
admin.site.register(CPPSanctionAssessment)
admin.site.register(AccountType)
admin.site.register(VendorDetails)
admin.site.register(Status)
admin.site.register(StatusField)
admin.site.register(UserStatus)
admin.site.register(ActivityLog)
