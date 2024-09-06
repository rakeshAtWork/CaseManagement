from django.contrib import admin

from acl.models import (Role, UserRole, MasterPrivilege, RolePermission, AppConfiguration)

# from .models import *

# Register your models here.


admin.site.register(Role)
admin.site.register(UserRole)
admin.site.register(MasterPrivilege)
admin.site.register(RolePermission)
admin.site.register(AppConfiguration)
