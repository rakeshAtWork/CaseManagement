from django.core.cache import cache
from django.core.paginator import Paginator
from rest_framework.exceptions import ValidationError
from rest_framework.generics import (RetrieveAPIView, CreateAPIView, get_object_or_404, RetrieveUpdateDestroyAPIView,
                                     UpdateAPIView)
from django.http import JsonResponse
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from acl.export_excel import export_query_to_excel
from acl.privilege import CozentusPermission
from django.utils import timezone

from case_management.utility import log_activity
from .permissions import permission_user_list_view, permission_profile_details, permission_user_short_info, \
    permission_user_detail_edit
from .serializers import (UserSerializers, UserReadSerializer, UserShortInfoSerializer, UserSerializer,
                          AdminUserRegisterSerializer, UserPasswordSerializer,
                          UserForgotPasswordSerializer, OtpVerifySerializer, UserStatusSerializer,
                          UserPasswordResetSerializer, UserProfileReadSerializer, UserLoginSerializer,
                          )
from .models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema
import logging

logger = logging.getLogger(__name__)


class UserFilterApi(APIView):
    """
    This view class is used to return user details with filter and pagination
    """
    serializer_class = UserReadSerializer
    case_management_object_permissions = {
        'POST': (permission_user_list_view,)
    }

    permission_classes = (CozentusPermission,)

    @extend_schema(request=UserSerializers)
    def post(self, request):
        """
        This method takes body input and filter the data and return the data with pagination
        """
        try:
            logger.info("User List Filter Started.")
            page_size = request.data.get("page_size", 50)
            page = request.data.get("page", 1)
            if page < 1 or page_size < 1:
                logger.info("page and page size should be positive integer")
                return Response({"message": "page and page size should be positive integer"},
                                status=status.HTTP_400_BAD_REQUEST)

            # Retrieve filter and ordering parameters
            order_by = request.data.get('order_by', None)
            order_type = request.data.get('order_type', None)
            serializer = UserSerializers(data=request.data)
            serializer.is_valid(raise_exception=True)
            data = serializer.data

            user_status = data.get('status', None)
            is_active = data.get('is_active', None)

            # Define filter dictionary
            filter_dict = {
                "email": "email__icontains",
                "first_name": "first_name__icontains",
                "last_name": "last_name__icontains",
                "organization_name": "organization_name__icontains",
                "phone_number": "phone_number__icontains",
                "status": "status",
                "role": "role_user__role__role_name__icontains"
            }

            # Generate query dictionary based on provided data
            query_dict = {filter_dict.get(key, None): value for key, value in data.items() if
                          value or isinstance(value, (int, float))}
            query_dict = {key: value for key, value in query_dict.items() if key}
            query_dict["is_delete"] = False

            # Filter queryset by is_active status
            if is_active is not None:
                query_dict['is_active'] = is_active

            queryset = CustomUser.objects.filter(**query_dict).order_by("first_name")

            # Apply user_status filter if provided
            if user_status == 0:
                queryset = queryset.filter(is_active=False)
            elif user_status == 1:
                queryset = queryset.filter(is_active=True)

            # Define ordering dictionary
            order_by_dict = {
                "is_active": "is_active",
                "email": "email",
                "first_name": "first_name",
                "last_name": "last_name",
                "is_delete": "is_delete",
                "organization_name": "organization_name",
                "phone_number": "phone_number",
                "created_on": "created_on",
                "last_login": "last_login",
                "created_by": "created_by",
                "role": "role_user__role__role_name"
            }

            # Apply ordering based on provided parameters
            query_filter = order_by_dict.get(order_by, None)
            if order_type == "desc" and query_filter:
                query_filter = "-%s" % query_filter
            if query_filter:
                queryset = queryset.order_by(query_filter)

            # Handle data export
            if data.get("export"):
                serializer = self.serializer_class(queryset, many=True, context=self.request)
                return export_query_to_excel(data=serializer.data, module_name="USER_MANAGEMENT")

            # Apply pagination
            paginator = Paginator(queryset, page_size)
            number_pages = paginator.num_pages
            if page > number_pages and page > 1:
                logger.info("Page Not Found")
                return Response({"message": "Page not found"}, status=status.HTTP_400_BAD_REQUEST)

            # Serialize and return paginated results
            page_obj = paginator.get_page(page)
            serializer = self.serializer_class(page_obj, many=True, context=self.request)
            data = serializer.data
            logger.info("User List Filter Successfully completed.")
            return Response({"count": queryset.count(), "results": data}, status=status.HTTP_200_OK)

        except Exception as ee:
            logger.warning(str(ee))
            return Response(str(ee), status=status.HTTP_400_BAD_REQUEST)


class UserDetailApi(RetrieveAPIView):
    """
    This view class is used to view an existing user
    """
    case_management_object_permissions = {
        'GET': (permission_profile_details,)
    }
    permission_classes = (CozentusPermission,)
    serializer_class = UserReadSerializer
    queryset = CustomUser.objects.all()


class UserShortInfoApi(RetrieveAPIView):
    """
    This view class is used to view an existing user for less info
    """
    case_management_object_permissions = {
        'GET': (permission_user_short_info,)
    }
    permission_classes = (CozentusPermission,)
    serializer_class = UserShortInfoSerializer
    queryset = CustomUser.objects.all()


class UserProfileApi(APIView):
    """
    This view class is used to view an existing user
    """
    case_management_object_permissions = {
        'GET': (permission_profile_details,)
    }
    permission_classes = (CozentusPermission,)
    serializer_class = UserProfileReadSerializer
    queryset = CustomUser.objects.all()

    # def get_object(self):
    #     queryset = self.get_queryset()
    #     obj = get_object_or_404(queryset, email=self.request.user.email)
    #     return obj
    def get(self, request):
        """
        Fetch and return the profile details of the currently logged-in user.
        """
        user = request.user  # Get the currently logged-in user from the request

        # Ensure the user is authenticated
        if not user.is_authenticated:
            return Response({"message": "User is not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = self.serializer_class(user, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class CurrentUserProfileApi(APIView):
    """
    This view class is used to view an existing user
    """
    case_management_object_permissions = {
        'GET': (permission_profile_details,)
    }
    permission_classes = (CozentusPermission,)
    serializer_class = UserProfileReadSerializer
    queryset = CustomUser.objects.all()

    # def get_object(self):
    #     queryset = self.get_queryset()
    #     obj = get_object_or_404(queryset, email=self.request.user.email)
    #     return obj
    def get(self, request):
        """
        Fetch and return the profile details of the currently logged-in user.
        """
        user = request.user  # Get the currently logged-in user from the request

        # Ensure the user is authenticated
        if not user.is_authenticated:
            return Response({"message": "User is not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = self.serializer_class(user, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class RegisterApi(CreateAPIView):
    """
    New user register API view
    """
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()

    def perform_create(self, serializer):
        try:
            # Save the new user instance
            instance = serializer.save(created_by=self.request.user.id)

            # Log the activity
            log_activity(
                instance=instance,
                request=self.request,
                action_type='CREATE',
                before_instance=None,
                after_instance=instance,
                description="User Registered",
            )
        except Exception as e:
            logger.error(f"An error occurred while registering the user: {str(e)}")
            raise serializers.ValidationError({
                "message": "An error occurred while registering the user.",
                "error": [str(e)]
            })


class UserUpdateApi(RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a user
    """
    permission_classes = (CozentusPermission,)
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()
    lookup_field = 'id'

    def perform_update(self, serializer):
        # Save the updated user instance
        user_instance = serializer.save(modified_by=self.request.user.id, modified_on=timezone.now())

        # Ensure user_instance.id is an integer
        if not isinstance(user_instance.id, int):
            logger.error(f"Expected integer ID but got {type(user_instance.id)}")
            raise ValueError("Invalid user ID type")

        # Log the update action
        logger.info(f"User {user_instance.id} updated by {self.request.user.id}.")

        try:
            # Retrieve the instance before update for activity log
            before_instance = CustomUser.objects.get(id=user_instance.id)
        except CustomUser.DoesNotExist:
            logger.error(f"User {user_instance.id} does not exist before update.")
            before_instance = None  # Handle if the instance does not exist

        # Log activity
        log_activity(
            instance=user_instance,
            request=self.request,
            action_type='UPDATE',
            before_instance=before_instance,
            after_instance=user_instance,
            description="User updated"
        )

    def perform_destroy(self, instance):
        try:
            # Retrieve the instance before soft deletion for activity log
            before_instance = CustomUser.objects.get(id=instance.id)

            # Perform the soft delete
            instance.is_delete = True
            instance.save()

            # Log the soft deletion action
            logger.info(f"User {instance.id} soft-deleted by {self.request.user.id}.")

            # Log activity
            log_activity(
                instance=instance,
                request=self.request,
                action_type='DELETE',
                before_instance=before_instance,
                after_instance=instance,  # After soft-delete, instance is the same as before
                description="User soft-deleted"
            )
        except CustomUser.DoesNotExist:
            logger.error(f"User {instance.id} does not exist.")
        except Exception as e:
            logger.warning(f"Failed to soft-delete user {instance.id}: {str(e)}")
            raise


class RegisterUserApi(CreateAPIView):
    """
    New user register by admin api view
    """
    permission_classes = (CozentusPermission,)
    serializer_class = AdminUserRegisterSerializer
    queryset = CustomUser.objects.all()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user.id)


class UserChangePasswordApi(UpdateAPIView):
    """
    change password of user api view
    """
    case_management_object_permissions = {
        'PUT': (permission_user_detail_edit,),
        'PATCH': (permission_user_detail_edit,),
    }
    permission_classes = (CozentusPermission,)
    serializer_class = UserPasswordSerializer
    queryset = CustomUser.objects.filter(is_delete=False)

    def perform_update(self, serializer):
        serializer.save(modified_by=self.request.user)

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, id=self.request.user.id)
        return obj


class UserForgotPasswordApi(UpdateAPIView):
    """
    change password of user api view
    """
    permission_classes = (AllowAny,)
    serializer_class = UserForgotPasswordSerializer
    queryset = CustomUser.objects.filter(is_delete=False)
    lookup_field = 'email'


class UserOtpVerifyApi(APIView):
    """
    OtpVerify api view
    """

    @swagger_auto_schema(request_body=OtpVerifySerializer)
    def post(self, request):
        try:
            serializer = OtpVerifySerializer(data=request.data)
            if serializer.is_valid():
                otp = request.data["otp"]
                email = request.data["email"]
                store_otp = cache.get(email)
                if store_otp == int(otp):
                    cache.delete(email)
                    cache.set(f'{email}_verify', True, 120)
                    return JsonResponse(
                        {'status': 'success', "message": f"Otp verify successfully"}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, 400)

        except Exception as e:
            print(e)
            return JsonResponse(
                {'status': 'failed', "message": f"Otp verification failed"}, status=status.HTTP_400_BAD_REQUEST)

        return JsonResponse(
            {'status': 'failed', "message": f"Otp verification failed"}, status=status.HTTP_400_BAD_REQUEST)


class UserStatusApiView(UpdateAPIView):
    """
    change is_active status of user api view
    """
    permission_classes = (CozentusPermission,)
    serializer_class = UserStatusSerializer
    queryset = CustomUser.objects.filter(is_delete=False)

    def perform_update(self, serializer):
        serializer.save(modified_by=self.request.user.id)


class UserPasswordResetApi(CreateAPIView):
    """
    Reset Password of user api view
    """
    permission_classes = (AllowAny,)
    serializer_class = UserPasswordResetSerializer
    queryset = CustomUser.objects.all()


class UserJsonDataAPI(APIView):
    permission_classes = (CozentusPermission,)

    def get(self, request):
        queryset = CustomUser.objects.values('id', 'first_name', 'last_name')
        user_dict = {user['id']: f"{user['first_name']} {user['last_name']}".strip() for user in queryset}
        return Response({"count": len(user_dict), "results": user_dict}, status=status.HTTP_200_OK)


class UserLoginApi(APIView):
    """
    OtpVerify api view..
    """

    # @swagger_auto_schema(request_body=UserLoginSerializer)  # OtpVerifySerializer)
    @extend_schema(request=UserLoginSerializer, responses=UserLoginSerializer)
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = serializer.validated_data
                refresh = RefreshToken.for_user(user)
                logger.info("Log-in Success.")
                return JsonResponse(
                    {'access': str(refresh.access_token), "message": f"Login successfully"},
                    status=status.HTTP_200_OK)
            except Exception as ve:
                logger.warning(str(ve))
                return JsonResponse({"message": f"Login failed"}, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
