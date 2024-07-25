from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Status(models.Model):
    """
    Status Model
    """
    name = models.CharField(max_length=150)
    status_code = models.IntegerField(default=0)
    color_code = models.CharField(max_length=150)
    highlight = models.IntegerField(default=0)
    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE,
                                   related_name="status_created_by")
    updated_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE,
                                   related_name="status_updated_by")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = models.Manager()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']
        db_table = "status"


class Category(models.Model):
    """
    Category Model
    """
    name = models.CharField(max_length=150)

    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE,
                                   related_name="category_created_by")
    updated_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE,
                                   related_name="category_updated_by")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = models.Manager()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']
        db_table = "category"


class ProjectManagement(models.Model):
    client_id = models.CharField(max_length=200)
    department_id = models.CharField(max_length=200)  # Foreignkey!!
    project_id = models.CharField(max_length=200)  # Foreignkey
    project_manager_primary = models.CharField(max_length=200)
    support_group_email = models.CharField(max_length=200)
    product_owner = models.CharField(max_length=200, null=True, blank=True)
    contact_name = models.CharField(max_length=200, null=True, blank=True)
    contact_email = models.CharField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(null=True)
    updated_by = models.PositiveIntegerField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True)

    objects = models.Manager()

    class Meta:
        ordering = ['-created_at']
        db_table = "project"


class Department(models.Model):
    """
    Department Model
    """
    department_name = models.CharField(max_length=150)
    department_code = models.CharField(max_length=150)
    department_type = models.CharField(max_length=150)

    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE,
                                   related_name="department_created_by")
    updated_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE,
                                   related_name="department_updated_by")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)

    objects = models.Manager()

    def __str__(self):
        return self.department_name

    class Meta:
        ordering = ['-created_at']
        db_table = "departments"


#
class SLA(models.Model):
    id = models.UUIDField(primary_key=True)
    department = models.CharField(max_length=200)  # Add Foreign-key of the Department Table
    ticket_type = models.CharField(max_length=200)  # Add Foreign-key of the Ticket Table
    priority = models.CharField(max_length=50)
    response_time = models.DurationField()
    resolution_time = models.DurationField()
    is_delete = models.BooleanField(default=False)
    created_by = models.IntegerField(null=True)
    updated_by = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    objects = models.Manager()

    class Meta:
        db_table = 'SLA'
        ordering = ['created_at']

class TicketType(models.Model):
    id = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=255, blank=False, null=False)
    is_active = models.BooleanField(default=False)
    created_by = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.IntegerField(null=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    objects = models.Manager()

    class Meta:
        db_table = 'ticket_type'

# class Ticket(models.Model):
#     ticket_no = models.CharField(max_length=10)
#     ticket_status = models.PositiveIntegerField()
#     ticket_header = models.CharField(max_length=200)
#     ticket_details = models.CharField(max_length=500)
#     on_behalf = models.PositiveIntegerField()
#     ticket_category = models.PositiveIntegerField()
#     ticket_type = models.ForeignKey(TicketType, on_delete=models.CASCADE, related_name='ticket_ticket_type')
#     department_id = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='ticket_department')
#     project_id = models.PositiveIntegerField()
#     ticket_priority = models.PositiveIntegerField()
#     assigned_to = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE,
#                                     related_name='ticket_assigned_to')
#     assigned_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE,
#                                     related_name='ticket_assigned_by')
#     assigned_at = models.DateTimeField(null=True, blank=True)
#     reassigned_reason = models.CharField(max_length=500, null=True, blank=True)
#     reassigned_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE,
#                                       related_name='ticket_reassigned_by')
#     reassigned_at = models.DateTimeField(null=True, blank=True)
#     reassigned_status = models.PositiveIntegerField(null=True)
#     hold_from = models.DateTimeField(null=True, blank=True)
#     hold_to = models.DateTimeField(null=True, blank=True)
#     cancellation_at = models.DateTimeField(null=True, blank=True)
#     response_within = models.DateTimeField(null=True, blank=True)
#     response_at = models.DateTimeField(null=True, blank=True)
#     response_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE,
#                                     related_name='ticket_response_by')
#     response_status = models.PositiveIntegerField(null=True)
#     response_breach = models.CharField(max_length=100, null=True, blank=True)
#     response_breach_time = models.DateTimeField(null=True, blank=True)
#     resolution_within = models.DateTimeField(null=True, blank=True)
#     resolution_postponed_time = models.DateTimeField(null=True, blank=True)
#     resolution_at = models.DateTimeField(null=True, blank=True)
#     resolution_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE,
#                                       related_name='ticket_resolution_by')
#     resolution_status = models.PositiveIntegerField(null=True)
#     resolution_breach = models.CharField(max_length=100, null=True, blank=True)
#     resolution_breach_time = models.DateTimeField(null=True, blank=True)
#     closed_at = models.DateTimeField(null=True, blank=True)
#     comments = models.CharField(max_length=500, null=True, blank=True)
#     tags = models.CharField(max_length=200, null=True, blank=True)
#     is_delete = models.BooleanField(null=True)
#     created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE,
#                                    related_name="ticket_created_by")
#     updated_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE,
#                                    related_name="ticket_updated_by")
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(null=True, blank=True)
#     deleted_at = models.DateTimeField(null=True, blank=True)
#
#     objects = models.Manager()
#
#     class Meta:
#         db_table = 'ticket'


# class TicketBehalf(models.Model):
#     ticket_id = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='ticket_behalf_ticket')
#     behalf_email = models.CharField(max_length=100)
#     created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE,
#                                    related_name="ticket_behalf_created_by")
#     updated_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE,
#                                    related_name="ticket_behalf_updated_by")
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(null=True, blank=True)
#     deleted_at = models.DateTimeField(null=True, blank=True)
#
#     objects = models.Manager()
#
#     class Meta:
#         db_table = 'ticket_behalf'


# class TicketFollower(models.Model):
#     ticket_id = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='ticket_follower_ticket')
#     follower_id = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE,
#                                     related_name="ticket_follower_follower_id")
#     created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE,
#                                    related_name="ticket_follower_created_by")
#     updated_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE,
#                                    related_name="ticket_follower_updated_by")
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(null=True, blank=True)
#     deleted_at = models.DateTimeField(null=True, blank=True)
#
#     objects = models.Manager()
#
#     class Meta:
#         db_table = 'ticket_follower'

#
# class TicketRevision(models.Model):
#     ticket_id = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='ticket_revision_ticket')
#     revision_status = models.PositiveIntegerField()
#     pti = models.PositiveIntegerField()
#     action_taken = models.DateTimeField()
#     before_revision = models.CharField(max_length=500)
#     after_revision = models.CharField(max_length=500)
#     created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE,
#                                    related_name="ticket_revision_created_by")
#     updated_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE,
#                                    related_name="ticket_revision_updated_by")
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(null=True, blank=True)
#     deleted_at = models.DateTimeField(null=True, blank=True)
#
#     objects = models.Manager()
#
#     class Meta:
#         db_table = 'ticket_revision'

# Create your models here.

#
#
# class UserDepartment(models.Model):
#     """
#     User Department Model
#     """
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_department_user")
#     department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="user_department_department")
#     created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE,
#                                    related_name="user_department_created_by")
#     updated_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE,
#                                    related_name="user_department_updated_by")
#     created_on = models.DateTimeField(auto_now_add=True)
#     updated_on = models.DateTimeField(null=True, blank=True)
#     is_delete = models.BooleanField(default=False)
#
#     objects = models.Manager()
#
#     class Meta:
#         ordering = ['-created_on']
#         unique_together = ('department', 'user',)
#         db_table = "user_department"
#
#
# # Create your models here.
# class TicketType(models.Model):
#     id = models.UUIDField(primary_key=True)
#     name = models.CharField(max_length=255, blank=False, null=False)
#     is_active = models.BooleanField(default=False)
#     created_by = models.IntegerField(null=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_by = models.IntegerField(null=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     deleted_at = models.DateTimeField(blank=True, null=True)
#
#     objects = models.Manager()
#
#     class Meta:
#         db_table = 'ticket_type'
#

#
#
# class Category(models.Model):
#     """
#     Category Model
#     """
#     name = models.CharField(max_length=150)
#
#     created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE,
#                                    related_name="category_created_by")
#     updated_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE,
#                                    related_name="category_updated_by")
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(null=True, blank=True)
#     deleted_at = models.DateTimeField(null=True, blank=True)
#
#     objects = models.Manager()
#
#     def __str__(self):
#         return self.name
#
#     class Meta:
#         ordering = ['-created_at']
#         db_table = "category"
#
#

# class ClientManagement(models.Model):
#     client_id = models.CharField(max_length=10)
#     client_name = models.CharField(max_length=200)
#     client_location = models.CharField(max_length=200)
#     contact_name = models.CharField(max_length=200)
#     contact_email = models.CharField(max_length=200)
#     created_at = models.DateTimeField(auto_now_add=True)
#     created_by = models.PositiveIntegerField()
#     client_status = models.BooleanField(default=True)
#     updated_at = models.DateTimeField(null=True)
#     updated_by = models.PositiveIntegerField(null=True, blank=True)
#     deleted_at = models.DateTimeField(null=True)
#
#     objects = models.Manager()
#
#     class Meta:
#         ordering = ['-created_at']
#         db_table = "client"
#
#
# class ProjectManagement(models.Model):
#     client_id = models.CharField(max_length=200)
#     department_id = models.CharField(max_length=200)  # Foreignkey!!
#     project_id = models.CharField(max_length=200)  # Foreignkey
#     project_manager_primary = models.CharField(max_length=200)
#     support_group_email = models.CharField(max_length=200)
#     product_owner = models.CharField(max_length=200, null=True, blank=True)
#     contact_name = models.CharField(max_length=200, null=True, blank=True)
#     contact_email = models.CharField(max_length=200, null=True, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     created_by = models.PositiveIntegerField()
#     is_active = models.BooleanField(default=True)
#     updated_at = models.DateTimeField(null=True)
#     updated_by = models.PositiveIntegerField(null=True, blank=True)
#     deleted_at = models.DateTimeField(null=True)
#
#     objects = models.Manager()
#
#     class Meta:
#         ordering = ['-created_at']
#         db_table = "project"
