from django.contrib import admin
from .models import FileType, Client, Customer, BusinessUnit, Vendor, Application

# Register your models here.
admin.site.register(FileType)
admin.site.register(Client)
admin.site.register(Customer)
admin.site.register(BusinessUnit)
admin.site.register(Vendor)
admin.site.register(Application)
