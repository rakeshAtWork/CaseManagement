from django.contrib import admin
from .models import Department, SLA, Ticket, TicketType, Priority, Category
# Register your models here.

admin.site.register(Department)
admin.site.register(SLA)
admin.site.register(Ticket)
admin.site.register(TicketType)
admin.site.register(Priority)
admin.site.register(Category)