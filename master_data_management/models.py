from django.db import models

# Create your models here.
import uuid

from django.db import models


# Create your models here.
class FileType(models.Model):
    status = models.BooleanField(default=False)
    file_type = models.CharField(max_length=255)
    file_extension = models.CharField(max_length=25)
    max_file_size = models.PositiveIntegerField()
    file_description = models.CharField(max_length=255, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.PositiveIntegerField()
    modified_on = models.DateTimeField(null=True, blank=True)
    modified_by = models.PositiveIntegerField(null=True)
    is_delete = models.BooleanField(default=False)

    objects = models.Manager()

    def __str__(self):
        return self.file_type

    class Meta:
        ordering = ['created_on']
        db_table = 'FILE_TYPE'


class Client(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    status = models.BooleanField(default=False)
    code = models.CharField(max_length=25)
    name = models.CharField(max_length=255)
    contact_name = models.CharField(max_length=255)
    contact_email = models.EmailField(null=True, blank=True)
    contact_number = models.CharField(max_length=15)
    is_delete = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.PositiveIntegerField()
    modified_on = models.DateTimeField(null=True, blank=True)
    modified_by = models.PositiveIntegerField(null=True)

    objects = models.Manager()

    class Meta:
        ordering = ['created_on']
        db_table = 'CLIENT'


DISPOSAL_ACTION_TYPE = (
    ("ARCHIVE", "ARCHIVE"),
    ("DELETE", "DELETE"),
    ("REVIEW", "REVIEW")

)


class Customer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    client_id = models.CharField(max_length=255, null=True, blank=True)
    status = models.BooleanField(default=False)
    code = models.CharField(max_length=25)
    name = models.CharField(max_length=255)
    contact_name = models.CharField(max_length=255)
    contact_email = models.EmailField(null=True, blank=True)
    contact_number = models.CharField(max_length=15)
    retention_period = models.PositiveIntegerField(null=True, blank=True)
    disposal_action = models.CharField(choices=DISPOSAL_ACTION_TYPE, max_length=50, null=True, blank=True)
    disposal_notification_period = models.PositiveIntegerField(null=True, blank=True)
    is_delete = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.PositiveIntegerField()
    modified_on = models.DateTimeField(null=True, blank=True)
    modified_by = models.PositiveIntegerField(null=True)

    objects = models.Manager()

    class Meta:
        ordering = ['created_on']
        db_table = 'CUSTOMER'


class BusinessUnit(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    client_id = models.CharField(max_length=255, null=True)
    code = models.CharField(max_length=25)
    name = models.CharField(max_length=255)
    contact_name = models.CharField(max_length=255)
    contact_email = models.EmailField(null=True, blank=True)
    contact_number = models.CharField(max_length=15)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.PositiveIntegerField()
    modified_on = models.DateTimeField(null=True, blank=True)
    modified_by = models.PositiveIntegerField(null=True)
    is_delete = models.BooleanField(default=False)
    status = models.BooleanField(default=True)

    objects = models.Manager()

    class Meta:
        ordering = ['created_on']
        db_table = 'BUSINESS_UNIT'


class Vendor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer_id = models.CharField(max_length=255, null=True, blank=True)
    status = models.BooleanField(default=False)
    code = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    contact_name = models.CharField(max_length=255, null=True, blank=True)
    contact_email = models.EmailField(null=True, blank=True)
    contact_number = models.CharField(max_length=15)
    retention_period = models.PositiveIntegerField(null=True, blank=True)
    disposal_action = models.CharField(choices=DISPOSAL_ACTION_TYPE, max_length=50, null=True, blank=True)
    disposal_notification_period = models.PositiveIntegerField(null=True, blank=True)
    is_delete = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.PositiveIntegerField()
    modified_on = models.DateTimeField(null=True, blank=True)
    modified_by = models.PositiveIntegerField(null=True)

    objects = models.Manager()

    class Meta:
        ordering = ['created_on']
        db_table = 'VENDOR'


class Application(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    status = models.BooleanField(default=False)
    code = models.CharField(max_length=25, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    contact_name = models.CharField(max_length=100, null=True, blank=True)
    contact_email = models.EmailField(null=True, blank=True)
    contact_number = models.CharField(max_length=20, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.PositiveIntegerField()
    modified_on = models.DateTimeField(null=True, blank=True)
    modified_by = models.PositiveIntegerField(null=True)
    is_delete = models.BooleanField(default=False)

    objects = models.Manager()

    class Meta:
        ordering = ['created_on']
        db_table = 'APPLICATION'
