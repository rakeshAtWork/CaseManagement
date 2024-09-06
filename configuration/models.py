from django.db import models
from case_management.utility import BaseModel


class ColumnConfiguration(BaseModel):
    label = models.CharField(max_length=255, null=True, blank=True)
    key = models.CharField(max_length=255, null=True, blank=True)
    is_disabled = models.BooleanField(default=True, null=True)
    width = models.CharField(max_length=255, null=True, blank=True)
    is_sortable = models.BooleanField(default=True, null=True)
    is_filterable = models.BooleanField(default=True, null=True)
    filter_type = models.CharField(max_length=255, null=True, blank=True)
    is_selected = models.BooleanField(default=True, null=True)
    module_id = models.PositiveIntegerField(null=True)
    user_id = models.PositiveIntegerField(null=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'COLUMN_CONFIGURATION'

