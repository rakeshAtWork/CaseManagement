from django.contrib import admin
from .models import (Status, StatusField, UserStatus, ActivityLog)

admin.site.register(Status)
admin.site.register(StatusField)
admin.site.register(UserStatus)
admin.site.register(ActivityLog)
