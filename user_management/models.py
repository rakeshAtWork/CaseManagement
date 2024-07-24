import uuid

from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError('The email must be set')
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


# Create your models here
class CustomUser(AbstractBaseUser):
    """
    Create and save a User Details.
    """
    username = None
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = None
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=15, null=True)
    client_id = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    organisation_name = models.CharField(max_length=15, blank=True, null=True)
    timezone = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    is_active = models.BooleanField(default=False)
    is_delete = models.BooleanField(default=False)
    is_application = models.BooleanField(default=False)

    last_login = models.DateTimeField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True, )
    created_by = models.IntegerField(null=True)
    modified_on = models.DateTimeField(null=True)
    modified_by = models.IntegerField(null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password']

    objects = CustomUserManager()

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        # Simplest possible answer: Yes, always
        return True

    class Meta:
        db_table = "CUSTOM_USER"
        ordering = ['first_name']


TOKEN_TYPES = (
    ("APP_TOKEN", "APP_TOKEN"),
    ("LOGIN_TOKEN", "LOGIN_TOKEN"),

)


class TokenModule(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user_id = models.OneToOneField(CustomUser, on_delete=models.DO_NOTHING, null=True,
                                   related_name="token_user_id")
    expiry_days = models.PositiveIntegerField(default=10)
    expiry_time = models.DateTimeField(null=True)
    type = models.CharField(max_length=255, choices=TOKEN_TYPES, default="APP_TOKEN")
    primary_token = models.CharField(max_length=120, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True, )
    created_by = models.IntegerField(null=True)
    modified_on = models.DateTimeField(null=True)
    modified_by = models.IntegerField(null=True)

    objects = models.Manager()

    class Meta:
        ordering = ['-created_on']
        db_table = 'TOKEN_MANAGEMENT'
