from django.contrib import admin
from .models import FileType, Client, Customer, BusinessUnit, Vendor, Application, VendorDetails, AccountType, \
    SupplierContactDetails, D365FOSetup, CompanyInfoForValidation, CPPSanctionAssessment

# Register your models here.
# admin.site.register(FileType)
# admin.site.register(Client)
# admin.site.register(Customer)
# admin.site.register(BusinessUnit)
# admin.site.register(Vendor)
# admin.site.register(Application)

admin.site.register(SupplierContactDetails)
admin.site.register(D365FOSetup)
admin.site.register(CompanyInfoForValidation)
admin.site.register(CPPSanctionAssessment)
admin.site.register(AccountType)
admin.site.register(VendorDetails)
