from django.contrib.auth import get_user_model
from django.db import models
from case_management.utility import StatusCodeEnum, BaseModel

User = get_user_model()


#
#
# class FileType(models.Model):
#     status = models.BooleanField(default=False)
#     file_type = models.CharField(max_length=255)
#     file_extension = models.CharField(max_length=25)
#     max_file_size = models.PositiveIntegerField()
#     file_description = models.CharField(max_length=255, null=True, blank=True)
#     created_on = models.DateTimeField(auto_now_add=True)
#     created_by = models.PositiveIntegerField()
#     modified_on = models.DateTimeField(null=True, blank=True)
#     modified_by = models.PositiveIntegerField(null=True)
#     is_delete = models.BooleanField(default=False)
#
#     objects = models.Manager()
#
#     def __str__(self):
#         return self.file_type
#
#     class Meta:
#         ordering = ['created_on']
#         db_table = 'FILE_TYPE'
#
#
# class Client(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     status = models.BooleanField(default=False)
#     code = models.CharField(max_length=25)
#     name = models.CharField(max_length=255)
#     contact_name = models.CharField(max_length=255)
#     contact_email = models.EmailField(null=True, blank=True)
#     contact_number = models.CharField(max_length=15)
#     is_delete = models.BooleanField(default=False)
#     created_on = models.DateTimeField(auto_now_add=True)
#     created_by = models.PositiveIntegerField()
#     modified_on = models.DateTimeField(null=True, blank=True)
#     modified_by = models.PositiveIntegerField(null=True)
#
#     objects = models.Manager()
#
#     class Meta:
#         ordering = ['created_on']
#         db_table = 'CLIENT'
#
#
# DISPOSAL_ACTION_TYPE = (
#     ("ARCHIVE", "ARCHIVE"),
#     ("DELETE", "DELETE"),
#     ("REVIEW", "REVIEW")
#
# )
#
#
# class Vendor(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     customer_id = models.CharField(max_length=255, null=True, blank=True)
#     status = models.IntegerField(default=False)
#     code = models.CharField(max_length=255)
#     name = models.CharField(max_length=255)
#     contact_name = models.CharField(max_length=255, null=True, blank=True)
#     contact_email = models.EmailField(null=True, blank=True)
#     contact_number = models.CharField(max_length=15)
#     retention_period = models.PositiveIntegerField(null=True, blank=True)
#     disposal_action = models.CharField(choices=DISPOSAL_ACTION_TYPE, max_length=50, null=True, blank=True)
#     disposal_notification_period = models.PositiveIntegerField(null=True, blank=True)
#     is_delete = models.BooleanField(default=False)
#     created_on = models.DateTimeField(auto_now_add=True)
#     created_by = models.PositiveIntegerField()
#     modified_on = models.DateTimeField(null=True, blank=True)
#     modified_by = models.PositiveIntegerField(null=True)
#
#     objects = models.Manager()
#
#     class Meta:
#         ordering = ['created_on']
#         db_table = 'VENDOR'
#
#
# class Customer(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     client_id = models.CharField(max_length=255, null=True, blank=True)
#     status = models.BooleanField(default=False)
#     code = models.CharField(max_length=25)
#     name = models.CharField(max_length=255)
#     contact_name = models.CharField(max_length=255)
#     contact_email = models.EmailField(null=True, blank=True)
#     contact_number = models.CharField(max_length=15)
#     retention_period = models.PositiveIntegerField(null=True, blank=True)
#     disposal_action = models.CharField(choices=DISPOSAL_ACTION_TYPE, max_length=50, null=True, blank=True)
#     disposal_notification_period = models.PositiveIntegerField(null=True, blank=True)
#     is_delete = models.BooleanField(default=False)
#     created_on = models.DateTimeField(auto_now_add=True)
#     created_by = models.PositiveIntegerField()
#     modified_on = models.DateTimeField(null=True, blank=True)
#     modified_by = models.PositiveIntegerField(null=True)
#
#     objects = models.Manager()
#
#     class Meta:
#         ordering = ['created_on']
#         db_table = 'CUSTOMER'
#
#
# class BusinessUnit(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     client_id = models.CharField(max_length=255, null=True)
#     code = models.CharField(max_length=25)
#     name = models.CharField(max_length=255)
#     contact_name = models.CharField(max_length=255)
#     contact_email = models.EmailField(null=True, blank=True)
#     contact_number = models.CharField(max_length=15)
#     created_on = models.DateTimeField(auto_now_add=True)
#     created_by = models.PositiveIntegerField()
#     modified_on = models.DateTimeField(null=True, blank=True)
#     modified_by = models.PositiveIntegerField(null=True)
#     is_delete = models.BooleanField(default=False)
#     status = models.BooleanField(default=True)
#
#     objects = models.Manager()
#
#     class Meta:
#         ordering = ['created_on']
#         db_table = 'BUSINESS_UNIT'
#

# class Application(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     status = models.BooleanField(default=False)
#     code = models.CharField(max_length=25, null=True, blank=True)
#     name = models.CharField(max_length=255, null=True, blank=True)
#     contact_name = models.CharField(max_length=100, null=True, blank=True)
#     contact_email = models.EmailField(null=True, blank=True)
#     contact_number = models.CharField(max_length=20, null=True, blank=True)
#     created_on = models.DateTimeField(auto_now_add=True)
#     created_by = models.PositiveIntegerField()
#     modified_on = models.DateTimeField(null=True, blank=True)
#     modified_by = models.PositiveIntegerField(null=True)
#     is_delete = models.BooleanField(default=False)
#
#     objects = models.Manager()
#
#     class Meta:
#         ordering = ['created_on']
#         db_table = 'APPLICATION'


# class AccountType(models.Model):
#     ACCOUNT_CHOICES = (
#         ('IBAN', 'IBAN'),
#         ('Domestic', 'Domestic'),
#     )
#     account_type = models.CharField(max_length=10, choices=ACCOUNT_CHOICES)
#     # vendor = models.OneToOneField(VendorDetails, on_delete=models.CASCADE, related_name='account_types', blank=True,
#     #                               null=True)
#     # created_by = models.PositiveIntegerField()
#     # modified_by = models.PositiveIntegerField()
#     # created_on = models.DateTimeField(auto_now_add=True)
#     # modified_on = models.DateTimeField(auto_now=True)
#     is_delete = models.BooleanField(default=False)
#
#     objects = models.Manager()
#
#     class Meta:
#         db_table = 'ACCOUNT_TYPE'


# class SupplierContactDetails(models.Model):
#     contact_person = models.CharField(max_length=255)
#     main_phone_number = models.CharField(max_length=20)
#     main_email_id = models.EmailField()
#     finance_phone_number = models.CharField(max_length=20, blank=True, null=True)
#     finance_email_id = models.EmailField(blank=True, null=True)
#     remittance_email_id = models.EmailField(blank=True, null=True)
#     email_for_receiving_po = models.EmailField(blank=True, null=True)
#     email_id_for_quote = models.EmailField(blank=True, null=True)
#     created_by = models.PositiveIntegerField()
#     modified_by = models.PositiveIntegerField(blank=True, null=True)
#     created_on = models.DateTimeField(auto_now_add=True)
#     modified_on = models.DateTimeField(auto_now=True)
#     is_delete = models.BooleanField(default=False)
#
#     objects = models.Manager()
#
#     class Meta:
#         db_table = 'SUPPLIER_CONTACT_DETAILS'

#
# class D365FOSetup(models.Model):
#     sales_tax_group = models.CharField(max_length=255)
#     vendor_group = models.CharField(max_length=255)
#     payment_method = models.CharField(max_length=255)
#     business_unit = models.CharField(max_length=255)
#     inter_company = models.BooleanField(default=False)
#     vendor_hold = models.BooleanField(default=False)
#     source_system = models.CharField(max_length=255)
#     source_system_supplier_reference = models.CharField(max_length=255)
#     d365fo_id = models.CharField(max_length=255)
#     fs_ticket_number = models.CharField(max_length=255)
#     allow_false_duplicates = models.BooleanField(default=False)
#     additional_comments = models.TextField(blank=True, null=True)
#     created_by = models.PositiveIntegerField()
#     modified_by = models.PositiveIntegerField(blank=True, null=True)
#     created_on = models.DateTimeField(auto_now_add=True)
#     modified_on = models.DateTimeField(auto_now=True)
#     is_delete = models.BooleanField(default=False)
#
#     objects = models.Manager()
#
#     class Meta:
#         db_table = 'D365FO_SETUP'


# class CompanyInfoForValidation(models.Model):
#     orbis_supplier = models.CharField(max_length=255)
#     orbis_bvd = models.CharField(max_length=255)
#     vat_supplier = models.CharField(max_length=255)
#     vat_validity = models.CharField(max_length=255)
#     vat_validity_date = models.DateField()
#     # vendor = models.OneToOneField(VendorDetails, on_delete=models.CASCADE, related_name='validation_info')
#     # created_by = models.PositiveIntegerField()
#     # modified_by = models.PositiveIntegerField()
#     # created_on = models.DateTimeField(auto_now_add=True)
#     # modified_on = models.DateTimeField(auto_now=True)
#     is_delete = models.BooleanField(default=False)
#
#     objects = models.Manager()
#
#     class Meta:
#         db_table = 'COMPANY_INFO_FOR_VALIDATION'
#
#
# class CPPSanctionAssessment(models.Model):
#     cfra_score = models.CharField(max_length=255)
#     cfra_portfolio_id = models.CharField(max_length=255)
#     cfra_score_card = models.CharField(max_length=255)
#     cfra_assessment = models.CharField(max_length=255)
#     # vendor = models.OneToOneField(VendorDetails, on_delete=models.CASCADE, related_name='sanction_assessments')
#     # created_by = models.PositiveIntegerField()
#     # modified_by = models.PositiveIntegerField()
#     # created_on = models.DateTimeField(auto_now_add=True)
#     # modified_on = models.DateTimeField(auto_now=True)
#     is_delete = models.BooleanField(default=False)
#
#     objects = models.Manager()
#
#     class Meta:
#         db_table = 'CPP_SANCTION_ASSESSMENT'
#
#
# class VendorDetails(models.Model):
#     company_code = models.CharField(max_length=255)
#     company_name = models.CharField(max_length=255)
#     agent_number = models.CharField(max_length=255)
#     supplier_type = models.CharField(max_length=255)
#     currency = models.CharField(max_length=255)
#     terms_of_payment = models.CharField(max_length=255)
#     supplier_name = models.CharField(max_length=255)
#     siret_number = models.CharField(max_length=255)
#     vat_country_code = models.CharField(max_length=255)
#     orbis_id = models.CharField(max_length=255)
#     orbis_id_found = models.BooleanField(default=False)
#     address_line = models.CharField(max_length=255)
#     country = models.CharField(max_length=255)
#     postal_code = models.CharField(max_length=20)
#     town = models.CharField(max_length=255)
#     country_code = models.CharField(max_length=10)
#     swift_number = models.CharField(max_length=255)
#     account_type = models.OneToOneField(AccountType, on_delete=models.CASCADE,
#                                         related_name='vendor_details_account_type', blank=True, null=True)
#     supplier_contact_details = models.OneToOneField(SupplierContactDetails, on_delete=models.CASCADE,
#                                                     related_name='vendor_details_supplier', blank=True, null=True)
#     d365fo_setup = models.OneToOneField('D365FOSetup', on_delete=models.CASCADE, related_name='vendor_details_d365fo',
#                                         blank=True, null=True)
#     company_info_for_validation = models.OneToOneField(CompanyInfoForValidation, on_delete=models.CASCADE,
#                                                        related_name='vendor_details_company', blank=True, null=True)
#     cpp_sanction_assessment = models.OneToOneField(CPPSanctionAssessment, on_delete=models.CASCADE,
#                                                    related_name='vendor_details_sanction', blank=True, null=True)
#     is_prime_revenue = models.BooleanField(default=False)
#     created_by = models.PositiveIntegerField()
#     modified_by = models.PositiveIntegerField(blank=True, null=True)
#     created_on = models.DateTimeField(auto_now_add=True)
#     modified_on = models.DateTimeField(auto_now=True)
#     is_delete = models.BooleanField(default=False)
#
#     objects = models.Manager()
#
#     class Meta:
#         db_table = 'VENDOR_DETAILS'


class Country(models.Model):
    """
    Country details
    """
    country_name = models.CharField(unique=True, max_length=255)
    country_code = models.CharField(max_length=50)
    description = models.TextField(null=True)
    created_by = models.PositiveIntegerField(blank=True, null=True)
    modified_by = models.PositiveIntegerField(blank=True, null=True)
    modified_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)

    objects = models.Manager()

    class Meta:
        db_table = 'COUNTRY'


class Currency(models.Model):
    currency_name = models.CharField(max_length=100, unique=True)
    currency_code = models.CharField(max_length=10, unique=True)
    # country_code = models.CharField(max_length=10, unique=True)
    created_by = models.PositiveIntegerField(blank=True, null=True)
    modified_by = models.PositiveIntegerField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)

    objects = models.Manager()

    class Meta:
        db_table = 'CURRENCY'


class Category(models.Model):
    """
    Category Model
    """
    name = models.CharField(max_length=150)

    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE,
                                   related_name="category_created_by")
    modified_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE,
                                    related_name="category_updated_by")
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = models.Manager()

    class Meta:
        ordering = ['-created_on']
        db_table = "CATEGORY"


class Department(models.Model):
    """
    Department Model
    """
    department_name = models.CharField(max_length=150)
    department_code = models.CharField(max_length=150)
    # department_type = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="categories", blank=True,
    #                                     null=True, )
    # department_type = models.CharField(max_length=150)

    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE,
                                   related_name="department_created_by")
    modified_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE,
                                    related_name="department_updated_by")
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)

    objects = models.Manager()

    class Meta:
        ordering = ['-created_on']
        db_table = "DEPARTMENTS"


class UserDepartment(models.Model):
    """
    User Department Model
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_department_user")
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="user_department_department")
    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE,
                                   related_name="user_department_created_by")
    modified_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE,
                                    related_name="user_department_updated_by")
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(null=True, blank=True)
    is_delete = models.BooleanField(default=False)

    objects = models.Manager()

    class Meta:
        ordering = ['-created_on']
        unique_together = ('department', 'user',)
        db_table = "USER_DEPARTMENT"


class Status(models.Model):
    """
    Status Model
    """
    name = models.CharField(max_length=150, unique=True)
    status_code = models.IntegerField(choices=[(tag.value[0], tag.value[1]) for tag in StatusCodeEnum],
                                      default=StatusCodeEnum.VENDOR_CREATION_INITIATED.value[0])
    color_name = models.CharField(max_length=200, null=True, blank=True)
    color_code = models.CharField(max_length=150, null=True, blank=True)
    highlight = models.IntegerField(default=0)
    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE,
                                   related_name="status_created_by")
    modified_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE,
                                    related_name="status_updated_by")
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    objects = models.Manager()

    class Meta:
        ordering = ['-created_on']
        db_table = "STATUS"


class EmailTemplateType(models.Model):
    template_name = models.CharField(max_length=255, unique=True)
    created_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="email_template_type_created_by"
    )
    created_on = models.DateTimeField(auto_now_add=True)
    modified_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="email_template_type_modified_by"
    )
    modified_on = models.DateTimeField(auto_now=True)

    objects = models.Manager()


class EmailTemplate(models.Model):
    is_active = models.BooleanField(default=True)
    template_type = models.OneToOneField(
        EmailTemplateType,
        on_delete=models.CASCADE,
        related_name="email_template",
        null=True, blank=True
    )
    subject = models.CharField(max_length=255)
    email_to = models.CharField(max_length=255)
    cc = models.TextField(blank=True, null=True)  # Storing as comma-separated string
    bcc = models.TextField(blank=True, null=True)  # Storing as comma-separated string
    message = models.TextField()
    signature = models.TextField(blank=True, null=True)

    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE,
                                   related_name="email_template_created_by")
    modified_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE,
                                    related_name="email_template_updated_by")
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(null=True, blank=True)

    objects = models.Manager()

    class Meta:
        db_table = "EMAIL_TEMPLATE"


class UserStatus(models.Model):
    """
    UserStatus Model to keep track of the user and their current status
    """
    user_id = models.IntegerField()
    status_id = models.IntegerField()
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.IntegerField(null=True, blank=True)
    modified_on = models.DateTimeField(null=True, blank=True)
    modified_by = models.IntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    objects = models.Manager()

    class Meta:
        ordering = ['-created_on']
        db_table = "USER_STATUS"
        constraints = [
            models.UniqueConstraint(fields=['user_id', 'status_id'], name='unique_user_status')
        ]


class StatusField(models.Model):
    status_code = models.IntegerField()
    field_name = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, related_name='status_field_created', on_delete=models.SET_NULL, null=True,
                                   blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_by = models.ForeignKey(User, related_name='status_field_modified', on_delete=models.SET_NULL, null=True,
                                    blank=True)
    modified_on = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    class Meta:
        unique_together = ('status_code', 'field_name')
        db_table = 'STATUS_FIELDS'


class ActivityLog(models.Model):
    ACTION_TYPE_CHOICES = [
        ('UPDATE', 'Update'),
        ('DELETE', 'Delete'),
        ('LOGIN', 'Login'),
        ('LOGOUT', 'Logout'),
        ('CREATE', 'Create'),
        # Add more actions as needed
    ]

    module_id = models.CharField(max_length=255, null=True, blank=True)
    user_email_id = models.EmailField(null=True, blank=True)
    column_name = models.CharField(max_length=255)
    before_input = models.TextField(null=True, blank=True)
    after_input = models.TextField(null=True, blank=True)
    action_type = models.CharField(max_length=20, choices=ACTION_TYPE_CHOICES)
    action_by = models.CharField(max_length=255, null=True, blank=True)
    action_date = models.DateTimeField(auto_now_add=True)
    table_name = models.CharField(max_length=255)
    description = models.TextField()
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    # module_item_id = models.CharField(max_length=255)
    remote_url = models.URLField()
    user_agent = models.CharField(max_length=512, null=True, blank=True)

    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE,
                                   related_name="activity_log_created_by")
    modified_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE,
                                    related_name="activity_log_modified_by")
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    objects = models.Manager()

    class Meta:
        db_table = 'ACTIVITY_LOG'

    def __str__(self):
        return f"{self.module_id} - {self.action_type} by {self.created_by.first_name} on {self.action_date}"


class LineOfBusiness(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)

    objects = models.Manager()

    class Meta:
        db_table = 'LINE_OF_BUSINESS'

    def __str__(self):
        return self.name


class LegalEntity(BaseModel):
    legal_entity_id = models.CharField(max_length=50, verbose_name="Legal Entity ID")
    legal_entity_name = models.CharField(max_length=255, verbose_name="Legal Entity Name")
    address_city = models.CharField(max_length=255, blank=True, null=True, verbose_name="Address City")
    address_country_region_id = models.CharField(max_length=10, blank=True, null=True,
                                                 verbose_name="Address Country Region ID")
    address_country_region_iso_code = models.CharField(max_length=5, blank=True, null=True,
                                                       verbose_name="Address Country Region ISO Code")
    address_description = models.TextField(verbose_name="Address Description", blank=True, null=True)
    address_street = models.CharField(max_length=255, blank=True, null=True, verbose_name="Address Street")
    address_zip_code = models.CharField(max_length=20, blank=True, null=True, verbose_name="Address ZIP Code")
    vendor_account_number = models.CharField(max_length=50, verbose_name="Vendor Account Number")
    sales_tax_group_code = models.CharField(max_length=50, verbose_name="Sales Tax Group Code", blank=True, null=True)
    bank_account_id = models.CharField(max_length=50, verbose_name="Bank Account ID", blank=True, null=True)
    currency_code = models.CharField(max_length=10, verbose_name="Currency Code")
    on_hold_status = models.CharField(max_length=50, verbose_name="On Hold Status", blank=True, null=True)
    vendor_group_id = models.CharField(max_length=50, verbose_name="Vendor Group ID", blank=True, null=True)
    vendor_hold_release_date = models.DateTimeField(verbose_name="Vendor Hold Release Date", blank=True, null=True)
    vendor_organization_name = models.CharField(max_length=255, verbose_name="Vendor Organization Name", blank=True,
                                                null=True)
    vendor_type = models.CharField(max_length=50, verbose_name="Vendor Type", blank=True, null=True)
    vend_source_system = models.CharField(max_length=50, verbose_name="Vendor Source System", blank=True, null=True)
    vend_source_system_id = models.CharField(max_length=50, verbose_name="Vendor Source System ID", blank=True,
                                             null=True)
    vat_number = models.CharField(max_length=50, verbose_name="VAT Number", blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)
    objects = models.Manager()

    class Meta:
        db_table = 'LEGAL_ENTITY'
        verbose_name = "Legal Entity"
        verbose_name_plural = "Legal Entities"
        ordering = ['legal_entity_name']

    def __str__(self):
        return self.legal_entity_name


class Vendor(BaseModel):
    vat_number = models.CharField(max_length=50, unique=True)
    dfds_entity_code = models.IntegerField()
    currency = models.IntegerField()
    supplier_source_system = models.IntegerField()
    supplier_type = models.CharField(max_length=50)

    class Meta:
        db_table = 'VENDOR'


class ProductDetails(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name
