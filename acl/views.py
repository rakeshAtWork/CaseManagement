from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, serializers
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from .export_excel import export_query_to_excel
from .permissions import permission_role_list, permission_role_create, permission_role_view, permission_role_edit, \
    permission_role_delete, permission_permission_list, permission_role_user_create, \
    permission_client_permission_create, permission_client_permission_view, permission_client_permission_edit, \
    permission_client_permission_delete, permission_client_permission_list
from .serializers import (RoleMultiUserCreateSerializer, RoleFilterSerializer, RoleReadSerializer,
                          RoleReadWithoutPrivilegeSerializer, RoleSerializer, RolePermissionFilterSerializer,
                          PermissionSerializer, ClientPrivilegeSerializer, ClientPrivilegeReadSerializer,
                          ClientPrivilegeFilterSerializer, )
from django.core.paginator import Paginator
from .models import Role, UserRole, MasterPrivilege, RolePermission, ClientPrivilege
from .privilege import CozentusPermission
from .classes import PermissionNamespace
from .auth import create_permission
import uuid

User = get_user_model()


class RoleFilterApi(APIView):
    """
    This view class is used to return  roles with filter and pagination
    """
    case_management_object_permissions = {
        'POST': (permission_role_list,)
    }
    permission_classes = (CozentusPermission,)
    serializer_class = RoleReadSerializer

    @swagger_auto_schema(request_body=RoleFilterSerializer)
    def post(self, request):
        """
        This method is used to make post request for pagination and filter and return the role data.
        """
        try:
            order_by = request.data.pop('order_by', None)
            order_type = request.data.pop('order_type', None)
            page_size = request.data.get("page_size", 50)
            page = request.data.get("page", 1)
            if page < 1 or page_size < 1:
                return Response({"message": "page and page size should be positive integer"},
                                status=status.HTTP_400_BAD_REQUEST)
            serializer = RoleFilterSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            data = serializer.data
            include_privilege_data = data.pop('include_privilege_data', True)

            filter_dict = {
                "role_name": "role_name__icontains", "role_description": "role_description__icontains",
                "client_id": "client_id"
            }

            dict_ = {filter_dict.get(key, None): value for key, value in data.items() if
                     value or isinstance(value, int)}
            dict_ = {key: value for key, value in dict_.items() if key}

            if request.user.client_id:

                dict_["client_id"] = request.user.client_id
            roles = Role.objects.filter(**dict_)
            order_by_dict = {
                "role_name": "role_name", "role_description": "role_description", "client_id": "client_id"
            }
            query_filter = order_by_dict.get(order_by, None)
            if order_type == "desc" and query_filter:
                query_filter = f"-{query_filter}"
            if query_filter:
                roles = roles.order_by(query_filter)
            if data.get("export"):
                results = RoleReadSerializer(roles, many=True)
                return export_query_to_excel(data=results.data, module_name="ROLE_MANAGEMENT")
            # Create Paginator object with page_size objects per page
            paginator = Paginator(roles, page_size)
            number_pages = paginator.num_pages
            if page > number_pages and page > 1:
                return Response({"message": "Page not found"}, status=status.HTTP_400_BAD_REQUEST)
            # Get the page object for the requested page number
            page_obj = paginator.get_page(page)
            if include_privilege_data:
                results = RoleReadSerializer(page_obj, many=True)
            else:
                results = RoleReadWithoutPrivilegeSerializer(page_obj, many=True)
            return Response({'count': roles.count(), 'results': results.data}, status=status.HTTP_200_OK)
        except serializers.ValidationError as ve:
            raise serializers.ValidationError(ve.detail)
        except Exception as ee:
            return Response(str(ee), status=status.HTTP_400_BAD_REQUEST)


class RoleCreateApi(CreateAPIView):
    """
    This view class is used to Create a new role
    """
    case_management_object_permissions = {
        'POST': (permission_role_create,)
    }
    permission_classes = (CozentusPermission,)
    serializer_class = RoleSerializer
    queryset = Role.objects.all()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user.id)


class RoleUpdateApi(RetrieveUpdateDestroyAPIView):
    """
    This view class is used to update an existing role
    """
    case_management_object_permissions = {
        'GET': (permission_role_view,),
        'PUT': (permission_role_edit,),
        'PATCH': (permission_role_edit,),
        'DELETE': (permission_role_delete,)
    }
    permission_classes = (CozentusPermission,)
    serializer_class = RoleSerializer
    queryset = Role.objects.all()

    def perform_update(self, serializer):
        serializer.save(modified_by=self.request.user.id)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance:
            if User.objects.filter(
                    id__in=UserRole.objects.filter(role=instance).values_list('user_id', flat=True),
                    is_delete=0).exists():
                return Response({"message": "This Role is currently associated with Single/Multiple Users!"},
                                status=status.HTTP_400_BAD_REQUEST)
            instance.delete()
            return Response({"message": "Role deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"message": "Record not found."}, status=status.HTTP_404_NOT_FOUND)


class RolePermissionFilterApi(APIView):
    """
    This view class is used to return role permission data with filter and pagination
    """
    case_management_object_permissions = {
        'POST': (permission_permission_list,)
    }
    permission_classes = (CozentusPermission,)
    serializer_class = RolePermissionFilterSerializer

    @swagger_auto_schema(request_body=RolePermissionFilterSerializer)
    def post(self, request):
        """
        This method is used for retrieving role permission data with pagination and filter
        """
        try:
            page_size = request.data.get("page_size", 200)
            page = request.data.get("page", 1)
            if page < 1 or page_size < 1:
                return Response({"message": "page and page size should be positive integer"},
                                status=status.HTTP_400_BAD_REQUEST)
            privilege_name = request.data.get('privilege_name')
            privilege_desc = request.data.get('privilege_desc')
            role_id = request.data.get('role_id')
            order_by = request.data.get('order_by')
            order_type = request.data.get('order_type')
            # Perform filtering based on the provided parameters
            queryset = MasterPrivilege.objects.all()
            if role_id:
                role_permission = RolePermission.objects.filter(role__id=role_id).values_list("privilege", flat=True)
                queryset = queryset.filter(id__in=role_permission)
            if privilege_name:
                queryset = queryset.filter(privilege_name__icontains=privilege_name)

            if privilege_desc:
                queryset = queryset.filter(privilege_desc__icontains=privilege_desc)
            if order_by in ["privilege_name", "privilege_desc"]:
                if order_type == "desc":
                    order_by = f"-{order_by}"
                queryset.order_by(order_by)
            if request.data.get("export"):
                results = PermissionSerializer(queryset, many=True)
                return export_query_to_excel(data=results.data, module_name="ROLE_PERMISSION")
            # Create Paginator object with page_size objects per page
            paginator = Paginator(queryset, page_size)
            number_pages = paginator.num_pages
            if page > number_pages:
                return Response({"message": "Page not found"}, status=status.HTTP_400_BAD_REQUEST)
            # Get the page object for the requested page number
            page_obj = paginator.get_page(page)
            serializer = PermissionSerializer(page_obj, many=True)  # RolePermissionSerializer(privileges, many=True)
            return Response({"count": len(queryset), "results": serializer.data})
        except serializers.ValidationError as ve:
            raise serializers.ValidationError(ve.detail)
        except Exception as ee:
            return serializers.ValidationError("Please provide valid data")


class RoleUserCreateAPI(CreateAPIView):
    """
    This view class is used to assign user a role
    """
    case_management_object_permissions = {
        'POST': (permission_role_user_create,)
    }
    permission_classes = (CozentusPermission,)
    serializer_class = RoleMultiUserCreateSerializer

    @swagger_auto_schema(request_body=RoleMultiUserCreateSerializer)
    def post(self, request):
        """
        This method is used for retrieving role permission data with pagination and filter
        """
        try:
            serializer = RoleMultiUserCreateSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            data = serializer.data
            user_ids = data.get("user_ids", [])
            role_id = data.get("role_id", "")
            updated_data = []
            role_object = Role.objects.filter(id=role_id).first()
            role_user_list = UserRole.objects.filter(role=role_object).values_list("user", flat=True)

            first_set = set(role_user_list)
            second_set = set(user_ids)
            remove_user = first_set - second_set
            add_user = second_set - first_set
            with transaction.atomic():
                if remove_user:
                    UserRole.objects.filter(user__id__in=list(remove_user)).delete()
                for user_id in list(add_user):
                    updated_data.append(UserRole(role=role_object,
                                                 user=User.objects.filter(id=user_id).first()))
                if updated_data:
                    UserRole.objects.bulk_create(updated_data)

            return Response({"results": data}, status=status.HTTP_201_CREATED)
        except serializers.ValidationError as ve:
            return Response({"message": ve.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ee:
            return Response({"message": "Please provide valid user data or role data"},
                            status=status.HTTP_400_BAD_REQUEST)


class ClientPrivilegeApi(CreateAPIView):
    """
    Client Privilege Create api view
    """
    case_management_object_permissions = {
        'POST': (permission_client_permission_create,)
    }
    permission_classes = [CozentusPermission]
    serializer_class = ClientPrivilegeSerializer
    queryset = ClientPrivilege.objects.all()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user.id)


class ClientPrivilegeModifyApi(RetrieveUpdateDestroyAPIView):
    """
    Client Privilege Modify api view
    """
    case_management_object_permissions = {
        'GET': (permission_client_permission_view,),
        'PUT': (permission_client_permission_edit,),
        'PATCH': (permission_client_permission_edit,),
        'DELETE': (permission_client_permission_delete,)
    }
    permission_classes = [CozentusPermission]
    serializer_class = ClientPrivilegeSerializer
    queryset = ClientPrivilege.objects.all()

    def perform_update(self, serializer):
        serializer.save(modified_by=self.request.user.id,
                        modified_on=timezone.now().astimezone(timezone.timezone.utc))


class ClientPrivilegeFilterApi(APIView):
    """
    Client Privilege filter api
    """
    case_management_object_permissions = {
        'POST': (permission_client_permission_list,),
    }
    permission_classes = (CozentusPermission,)
    serializer_class = ClientPrivilegeReadSerializer

    @swagger_auto_schema(request_body=ClientPrivilegeFilterSerializer)
    def post(self, request):
        """
        This method is used for retrieving role permission data with pagination and filter
        """
        serializer = ClientPrivilegeFilterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        try:
            page_size = request.data.get("page_size", 200)
            page = request.data.get("page", 1)
            if page < 1 or page_size < 1:
                return Response({"message": "page and page size should be positive integer"},
                                status=status.HTTP_400_BAD_REQUEST)
            order_by = request.data.get('order_by')
            order_type = request.data.get('order_type')

            filter_dict = {
                "privilege": "privilege", "client": "client",
                "created_on": "created_on", "created_by": "created_by",
                "modified_on": "modified_on", "modified_by": "modified_by"
            }
            query_dict = {filter_dict.get(key, None): value for key, value in data.items() if
                          value or isinstance(value, (int, bool))}
            query_dict = {key: value for key, value in query_dict.items() if key}
            print("Working till Here..")
            if request.user.client_id:
                query_dict["client"] = request.user.client_id

            queryset = ClientPrivilege.objects.filter(**query_dict).order_by('-created_on')
            order_dict = {
                "privilege": "privilege", "client": "client",
                "created_on": "created_on", "created_by": "created_by",
                "modified_on": "modified_on", "modified_by": "modified_by"
            }
            query_filter = order_dict.get(order_by, None)
            if query_filter:
                if order_type == "desc":
                    query_filter = f"-{query_filter}"
                queryset = queryset.order_by(query_filter)
            # if data.get("export"):
            #     results = self.serializer_class(queryset, many=True)
            #     return export_query_to_excel(data=results.data, module_name="CLIENT_PRIVILEGE")
            paginator = Paginator(queryset, page_size)
            number_pages = paginator.num_pages
            if page > number_pages:
                return Response({"message": "Page not found"}, status=status.HTTP_400_BAD_REQUEST)
            # Get the page object for the requested page number
            page_obj = paginator.get_page(page)
            serializer = self.serializer_class(page_obj, many=True)
            data = serializer.data
            return Response({"count": queryset.count(), "results": data})
        except Exception as ee:
            return Response({"message": "Something went wrong", "error": str(ee)}, status=status.HTTP_400_BAD_REQUEST)


class PopulatePermissionsView(APIView):
    permission_classes = [CozentusPermission]

    def post(self, request):
        permission_list = []
        for namespace in PermissionNamespace.get_all_namespaces():
            permission_list.extend(namespace.permissions)

        # print(permission_list)

        try:
            create_permission(permission_list)
            return Response({"message": "Permissions populated successfully."}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RoleDetailView(APIView):
    permission_classes = [CozentusPermission]

    def get(self, request, pk=None):
        if pk:
            try:
                uuid_role_id = uuid.UUID(pk)  # Convert pk to UUID
                role = Role.objects.get(id=uuid_role_id)
                serializer = RoleReadSerializer(role)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except ValueError:
                return Response({"error": "Invalid UUID format"}, status=status.HTTP_400_BAD_REQUEST)
            except Role.DoesNotExist:
                return Response({"error": "Role not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            roles = Role.objects.all()
            serializer = RoleReadSerializer(roles, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
