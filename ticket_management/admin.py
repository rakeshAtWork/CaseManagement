from django.contrib import admin
from .models import Department, SLA, Ticket
# Register your models here.

admin.site.register(Department)
admin.site.register(SLA)
admin.site.register(Ticket)