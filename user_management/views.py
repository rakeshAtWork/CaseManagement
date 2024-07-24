from django.core.cache import cache
from django.core.paginator import Paginator
from rest_framework.generics import (RetrieveAPIView, CreateAPIView, get_object_or_404, RetrieveUpdateDestroyAPIView,
                                     UpdateAPIView)
from django.http import JsonResponse
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from case_management.utility import get_random_string
from acl.export_excel import export_query_to_excel
from case_management.utility import generate_token
from .permissions import *
from acl.privilege import CozentusPermission
from django.utils import timezone
from .serializers import (UserSerializers, UserReadSerializer, UserShortInfoSerializer, UserSerializer,
                          AdminUserRegisterSerializer, UserEditSerializer, UserPasswordSerializer,
                          UserForgotPasswordSerializer, OtpVerifySerializer, UserStatusSerializer,
                          UserPasswordResetSerializer, UserProfileReadSerializer, UserLoginSerializer,
                          TokenSerializer, ResetTokenSerializer, )
from .models import CustomUser, TokenModule
from datetime import datetime, timedelta
from rest_framework_simplejwt.tokens import RefreshToken


class UserFilterApi(APIView):
    """
    This view class is used to return user details with filter and pagination
    """
    serializer_class = UserReadSerializer
    case_management_object_permissions = {
        'POST': (permission_user_list_view,)
    }

    permission_classes = (CozentusPermission,)

    @swagger_auto_schema(request_body=UserSerializers)
    def post(self, request):
        """
        This method takes body input and filter the data and return the data with pagination
        """
        try:
            page_size = request.data.get("page_size", 50)
            page = request.data.get("page", 1)
            if page < 1 or page_size < 1:
                return Response({"message": "page and page size should be positive integer"},
                                status=status.HTTP_400_BAD_REQUEST)
            order_by = request.data.get('order_by', None)
            order_type = request.data.get('order_type', None)
            serializer = UserSerializers(data=request.data)
            serializer.is_valid(raise_exception=True)
            data = serializer.data
            user_status = data.get('status', None)
            filter_dict = {
                "email": "email__icontains", "first_name": "first_name__icontains",
                "last_name": "last_name__icontains", "organization_name": "organization_name__icontains",
                "phone_number": "phone_number__icontains", "status": "is_active",
                "role": "role_user__role__role_name__icontains"
            }
            query_dict = {filter_dict.get(key, None): value for key, value in data.items() if
                          value or isinstance(value, (int, float))}
            query_dict = {key: value for key, value in query_dict.items() if key}
            query_dict["is_delete"] = False

            queryset = CustomUser.objects.filter(**query_dict).order_by("first_name")
            if user_status == 0:
                queryset = queryset.filter(is_active=0)
            elif user_status == 1:
                queryset = queryset.filter(is_active=1)
            order_by_dict = {
                "is_active": "is_active", "email": "email", "first_name": "first_name",
                "last_name": "last_name", "is_delete": "is_delete", "organization_name": "organization_name",
                "phone_number": "phone_number", "created_on": "created_on", "last_login": "last_login",
                "created_by": "created_by", "role": "role_user__role__role_name"
            }
            query_filter = order_by_dict.get(order_by, None)
            if order_type == "desc" and query_filter:
                query_filter = f"-{query_filter}"
            if query_filter:
                queryset = queryset.order_by(query_filter)
            if data.get("export"):
                serializer = self.serializer_class(queryset, many=True, context=self.request)
                return export_query_to_excel(data=serializer.data, module_name="USER_MANAGEMENT")
            # Create Paginator object with page_size objects per page
            paginator = Paginator(queryset, page_size)
            number_pages = paginator.num_pages
            if page > number_pages and page > 1:
                return Response({"message": "Page not found"}, status=status.HTTP_400_BAD_REQUEST)
            # Get the page object for the requested page number
            page_obj = paginator.get_page(page)
            serializer = self.serializer_class(page_obj, many=True, context=self.request)
            data = serializer.data

            return Response({"count": queryset.count(), "results": data}, status=status.HTTP_200_OK)
        except Exception as ee:
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


class UserProfileApi(RetrieveAPIView):
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


class RegisterApi(CreateAPIView):
    """
    New user register api view
    """
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user.id)


class RegisterUserApi(CreateAPIView):
    """
    New user register by admin api view
    """
    permission_classes = (CozentusPermission,)
    serializer_class = AdminUserRegisterSerializer
    queryset = CustomUser.objects.all()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user.id)


class UserModifyApi(RetrieveUpdateDestroyAPIView):
    """
    User Modify api of specific user from super admin user by providing user id
    """
    case_management_object_permissions = {
        'GET': (permission_profile_details,),
        'PUT': (permission_user_detail_edit,),
        'PATCH': (permission_user_detail_edit,),
        'DELETE': (permission_user_detail_delete,)
    }
    permission_classes = (CozentusPermission,)
    serializer_class = UserEditSerializer
    queryset = CustomUser.objects.filter(is_delete=False)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user.id)

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.is_delete = True
        instance.save()


class UserActionApi(RetrieveUpdateDestroyAPIView):
    """
    User update, delete and fetch api of current login user
    """
    case_management_object_permissions = {
        'GET': (permission_profile_details,),
        'PUT': (permission_user_detail_edit,),
        'PATCH': (permission_user_detail_edit,),
        'DELETE': (permission_user_detail_delete,)
    }
    permission_classes = (CozentusPermission,)
    queryset = CustomUser.objects.filter(is_delete=False)

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, email=self.request.user.email)
        return obj

    def get_serializer_class(self):
        if self.request.method == "GET":
            return UserReadSerializer
        else:
            return UserEditSerializer

    def perform_destroy(self, instance):
        if not instance.is_superuser:
            instance.is_active = False
            instance.is_delete = True
            instance.save()


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
        serializer.save(updated_by=self.request.user)

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

    @swagger_auto_schema(request_body=UserLoginSerializer)  # OtpVerifySerializer)
    def post(self, request):
        # Assuming you have received the request data and need to validate it and generate tokens
        # print(request.data)
        serializer = UserLoginSerializer(data=request.data)
        # print("Check serializer validity : ---", serializer.is_valid())
        if serializer.is_valid():
            # print("data is valid till here..")
            try:
                user = serializer.validated_data
                refresh = RefreshToken.for_user(user)
                # print("working till here 11")

                # token = generate_token(user_email=email)
                print("working till here 12")
                return JsonResponse(
                    {'access': str(refresh.access_token), "message": f"Login successfully"},
                    status=status.HTTP_200_OK)
            except Exception as ve:
                print(ve)
                return JsonResponse({"message": f"Login failed"}, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class GenerateTokenView(APIView):
    permission_classes = (CozentusPermission,)
    serializer_class = TokenSerializer

    @swagger_auto_schema(request_body=TokenSerializer)
    def post(self, request, *args, **kwargs):
        serializer = TokenSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data["created_by"] = request.user.id
            token_instance = serializer.save()
            return Response({
                'id': token_instance.id,
                'message': "primary token successfully generated.",
                'Token': token_instance.primary_token,
                'expiry_time': token_instance.expiry_time
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetTokenView(APIView):
    permission_classes = (CozentusPermission,)
    serializer_class = ResetTokenSerializer

    @swagger_auto_schema(request_body=ResetTokenSerializer)
    def post(self, request, *args, **kwargs):
        serializer = ResetTokenSerializer(data=request.data)
        if serializer.is_valid():
            user_id = serializer.validated_data['user_id']
            expiry_days = serializer.validated_data.get('expiry_days')

            token_id = kwargs.get('pk')

            try:
                token_instance = TokenModule.objects.get(id=token_id, user_id=user_id)
            except TokenModule.DoesNotExist:
                return Response({"detail": "Token not found for the given user."}, status=status.HTTP_404_NOT_FOUND)

            # Generate a new primary token
            token_instance.primary_token = get_random_string(length=120)

            # Update expiry time if expiry_days is provided
            if expiry_days:
                start_time = datetime.utcnow()
                token_instance.expiry_time = start_time + timedelta(days=expiry_days)

                token_instance.modified_on = timezone.now()
                token_instance.modified_by = request.user.id

            token_instance.save()

            return Response({
                'message': "Token reset successfully",
                'Token': token_instance.primary_token,
                'expiry_time': token_instance.expiry_time
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
