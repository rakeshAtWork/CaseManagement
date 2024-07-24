from django.utils import timezone
from rest_framework import serializers
import random
from threading import Thread
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import check_password
from django.core.cache import cache
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import make_password
from case_management.utility import new_user_registration_msg, get_random_string, email_send, \
    account_activate_new_password_msg
from acl.serializers import RoleShortInfoSerializer
# from case_management.graph_api import send_email_graph_api
from .models import CustomUser, TokenModule
from acl.models import UserRole, Role, RolePermission
from datetime import datetime, timedelta
from django.contrib.auth import authenticate, get_user_model
from django.core.validators import RegexValidator


class UserSerializers(serializers.ModelSerializer):
    """
    This Serializer  defines how the user take input in the api
    """
    page = serializers.IntegerField(required=False, allow_null=True, write_only=True)
    page_size = serializers.IntegerField(required=False, allow_null=True, write_only=True)
    email = serializers.CharField(max_length=100, required=False, allow_blank=True, allow_null=True)
    first_name = serializers.CharField(max_length=100, required=False, allow_blank=True, allow_null=True)
    role = serializers.CharField(max_length=100, required=False, allow_blank=True, allow_null=True)
    last_name = serializers.CharField(max_length=100, required=False, allow_blank=True, allow_null=True)
    organization_name = serializers.CharField(max_length=100, required=False, allow_blank=True, allow_null=True)
    phone_number = serializers.CharField(max_length=100, required=False, allow_blank=True, allow_null=True)
    order_by = serializers.CharField(max_length=100, required=False, allow_blank=True, allow_null=True, write_only=True)
    order_type = serializers.CharField(max_length=100, required=False, allow_blank=True, allow_null=True,
                                       write_only=True)

    status = serializers.IntegerField(required=False, allow_null=True)
    export = serializers.BooleanField(required=False, allow_null=True, default=False)

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'organization_name',
                  'phone_number', 'order_by', 'order_type', 'page', 'page_size', 'status', "role",
                  "export")


class UserReadSerializer(serializers.ModelSerializer):
    """
    This serializer is used on the time of responding data for user
    """
    role_data = serializers.SerializerMethodField(source='get_role_data', read_only=True)

    class Meta:
        model = CustomUser
        fields = ("id", "email", 'first_name', 'last_name', 'created_on', 'last_login', 'is_active',
                  'is_delete', 'phone_number', 'modified_on', "last_login", "organisation_name", "timezone",
                  "country", "created_by", "modified_by", "role_data")

    def get_role_data(self, obj):
        """
        This method is used for getting role data as per the user
        """
        role = UserRole.objects.filter(user=obj).values_list('role', flat=True)
        if not role:
            return []
        return RoleShortInfoSerializer(Role.objects.filter(id__in=role), read_only=True, context=self.context,
                                       many=True).data


class UserProfileReadSerializer(serializers.ModelSerializer):
    """
    This serializer is used on the time of responding data for user
    """
    role_data = serializers.SerializerMethodField(source='get_role_data', read_only=True)
    privileges = serializers.SerializerMethodField(source='get_privileges', read_only=True)

    class Meta:
        model = CustomUser
        fields = ("id", "email", 'first_name', 'last_name', 'created_on', 'last_login', 'is_active',
                  'is_delete', 'phone_number', 'modified_on', "last_login", "organisation_name", "timezone",
                  "country", "created_by", "modified_by", "role_data", "privileges")

    def get_role_data(self, obj):
        """
        This method is used for getting role data as per the user
        """
        role = UserRole.objects.filter(user=obj).values_list('role', flat=True)
        if not role:
            return []
        return RoleShortInfoSerializer(Role.objects.filter(id__in=role), read_only=True, context=self.context,
                                       many=True).data

    def get_privileges(self, obj):
        roles = UserRole.objects.filter(user=obj).values_list("role", flat=True)
        privilege = RolePermission.objects.filter(role__in=roles).values_list("privilege__privilege_name", flat=True)
        return privilege


class UserShortInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'first_name', 'last_name', "phone_number",)


class AdminUserRegisterSerializer(serializers.ModelSerializer):
    """
    Register new user by admin
    """

    class Meta:
        model = CustomUser
        fields = (
            'id', 'first_name', 'last_name', 'phone_number', 'email', 'password', 'is_active',
            'last_login', 'is_delete', "organisation_name", "timezone", "country")
        read_only_fields = ('is_active', 'last_login', 'is_delete')

    def validate_password(self, value: str) -> str:
        """
        Hash value passed by user.
        :param value: password of a user
        :return: a hashed version of the password
        """
        return make_password(value)

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])
        instance = super(AdminUserRegisterSerializer, self).create(validated_data)
        return instance


class UserSerializer(serializers.ModelSerializer):
    """
    Register new user model serializer
    """
    phone_number = serializers.CharField(
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',  # Example regex for international phone numbers
                message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
            )
        ]
    )

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'phone_number', 'email',
                  "organisation_name", "timezone", "country")

    def create(self, validated_data):
        random_password = get_random_string()
        validated_data["password"] = make_password(random_password)
        instance = super(UserSerializer, self).create(validated_data)
        try:
            print("trying to send an email to the user for password.")
            print(random_password)
            messages = new_user_registration_msg(user=instance)

            Thread(target=email_send, args=(instance.email, "New Registration", messages), ).start()
            # messages = new_user_registration_msg(user=instance)
            print("Email sent successfully..")
            # Thread(target=send_email_graph_api,
            #        args=("New Registration", messages, instance.email), ).start()
        except:
            print("Failed to send email to user")
            # print(e.msg)

        return instance


class UserPasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(
        required=True, style={'input_type': 'old password'}, write_only=True
    )
    new_password = serializers.CharField(
        required=True, style={'input_type': 'new password'}, write_only=True
    )

    class Meta:
        extra_kwargs = {
            'url': {'view_name': 'rest_api:user-detail'}
        }
        fields = (
            'old_password', 'new_password')
        model = CustomUser

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({"old_password": "Old password is not correct"})
        return value

    def validate_new_password(self, value):
        validate_password(value)
        return value

    def update(self, instance, validated_data):
        instance.set_password(validated_data['new_password'])
        instance.save()
        return instance


class UserForgotPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        extra_kwargs = {
            'url': {'view_name': 'rest_api:user-detail'}
        }
        fields = ('email',)
        model = CustomUser

    def update(self, instance, validated_data):
        random_key = random.randrange(100000, 999999, 6)
        # print(random_key)
        print("Random Key : ", random_key)
        # TODO password limit should add
        cache.set(instance.email, random_key, 60 * 15)
        try:
            messages = f"Your OTP for reset password : {random_key}"
            Thread(target=email_send, args=(instance.email, "Forget Password Request", messages), ).start()

            print("Sent email for reset password..")

        except:
            pass
        return instance


class UserStatusSerializer(serializers.ModelSerializer):
    class Meta:
        extra_kwargs = {
            'url': {'view_name': 'rest_api:user-status'},
            'is_active': {'required': False}
        }
        fields = ('is_active',)
        model = CustomUser

    def update(self, instance, validated_data):
        is_active = instance.is_active
        modified_by = validated_data.get("modified_by")
        if instance.email == self.context['request'].user.email:
            raise serializers.ValidationError({"msg": "You can't perform this operation with yourself"})
        instance.is_active = not is_active
        instance.modified_by = modified_by
        instance.modified_on = timezone.now().astimezone(timezone.timezone.utc)
        instance.save()
        if instance.is_active and not instance.last_login:
            random_password = get_random_string(length=12)
            print(random_password)
            instance.password = make_password(random_password)
            instance.save()
            # sending mail with active status and new_password is added
            messages = account_activate_new_password_msg(user=instance, new_password=random_password)
            Thread(target=email_send, args=(instance.email, "New Registration", messages), ).start()

        return instance


class UserEditSerializer(serializers.ModelSerializer):
    """
    perform retrieve, update serializer for user
    """

    class Meta:
        model = CustomUser
        fields = ('id', 'first_name', 'last_name', 'phone_number', 'email', 'password',
                  "organisation_name", "timezone", "country")


class UserPasswordResetSerializer(serializers.ModelSerializer):
    """
       User password reset Models serializer
       """
    password = serializers.CharField(
        required=True, style={'input_type': 'password'}, write_only=True
    )

    email = serializers.CharField(
        required=True, style={'input_type': 'user email'}, write_only=True
    )

    class Meta:
        fields = ('password', 'email')
        model = CustomUser

    def create(self, validated_data):
        try:
            if cache.get(f'{validated_data["email"]}_verify'):
                user_data = get_object_or_404(CustomUser.objects.all(), email=validated_data["email"])
                try:
                    validate_password(validated_data['password'], user_data)
                except Exception as exc:
                    raise serializers.ValidationError({"message": str(exc)})
                user_data.set_password(validated_data['password'])
                user_data.save()
                return user_data
            else:
                raise serializers.ValidationError({"message": "Password change time expired please retry new otp"})
        except IndexError:
            raise serializers.ValidationError({"message": "Password change time expired please retry new otp"})


class UserReadEmailSerializer(serializers.ModelSerializer):
    """
    Read user email model serializer
    """

    class Meta:
        model = CustomUser
        fields = ("id", "email", "first_name", "last_name")


class OtpVerifySerializer(serializers.Serializer):
    otp = serializers.IntegerField(
        required=True, style={'input_type': 'otp'}
    )
    email = serializers.CharField(
        required=True, style={'input_type': 'email'}
    )


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            try:
                user = CustomUser.objects.get(email=email)
                if not user.is_active:
                    raise serializers.ValidationError("Inactive user")
                if check_password(password, user.password):
                    return user
                else:
                    raise serializers.ValidationError("Incorrect password.")
            except CustomUser.DoesNotExist:
                raise serializers.ValidationError("User with this email does not exist.")
        else:
            raise serializers.ValidationError("Both email and password are required.")


#
# class UserLoginSerializer(serializers.Serializer):
#     email = serializers.EmailField()
#     password = serializers.CharField(style={'input_type': 'password'})
#
#     def validate(self, attrs):
#         email = attrs.get('email')
#         password = attrs.get('password')
#
#         if email and password:
#
#             user = CustomUser.objects.filter(email=email).first()
#             print("For validation ..", user.email, user.password, )
#             if user and not user.is_active:
#                 print("For validation .. User Invalid")
#                 raise serializers.ValidationError("Inactive user")
#             elif user and check_password(password, user.password):
#                 return user
#             else:
#                 raise serializers.ValidationError("Incorrect email or password.")
#         else:
#             raise serializers.ValidationError("Both email and password are required.")


# class UserLoginSerializer(serializers.Serializer):
#     email = serializers.EmailField()
#     password = serializers.CharField(write_only=True)
#
#     def validate(self, data):
#         email = data.get("email")
#         password = data.get("password")
#         User = get_user_model()
#
#         if email and password:
#             try:
#                 user = User.objects.get(email=email)
#             except User.DoesNotExist:
#                 raise serializers.ValidationError("Invalid email or password.")
#
#             if not check_password(password, user.password):
#                 raise serializers.ValidationError("Invalid email or password.")
#         else:
#             raise serializers.ValidationError("Must include both email and password.")
#
#         data["user"] = user
#         return data

class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = TokenModule
        fields = ("id", "user_id", "expiry_days", "expiry_time", "primary_token", "type",
                  "created_by", "created_on", "modified_by", "modified_on")
        read_only_fields = (
            "id", "primary_token", "expiry_time", "created_by", "created_on", "modified_by", "modified_on")

    def create(self, validated_data):
        validated_data["primary_token"] = get_random_string(length=120)
        expiry_days = validated_data.get("expiry_days")
        start_time = datetime.utcnow()
        expiry_time = start_time + timedelta(days=expiry_days)
        validated_data["expiry_time"] = expiry_time
        # validated_data["expiry_days"] = expiry_days
        instance = super().create(validated_data)

        return instance


class ResetTokenSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    expiry_days = serializers.IntegerField(required=False, min_value=1)
