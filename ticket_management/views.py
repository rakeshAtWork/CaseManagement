from rest_framework import generics
from .models import Department, SLA, Status, Category, ProjectManagement, TicketType, TicketFollower, TicketRevision, \
    Ticket
from .serializers import DepartmentSerializer, SLASerializer, StatusSerializer, StatusReadSerializer, \
    StatusFilterSerializer, CategorySerializer, \
    CategoryFilterSerializer, ProjectFilterSerializers, ProjectManagementReadSerializer, ProjectManagementSerializer, \
    SLAUpdateSerializer, DepartmentFilterSerializer, TicketTypeSerializer, TicketTypeUpdateSerializer, \
    TicketRevisionSerializer, TicketFollowerSerializer, TicketFollowerFilterSerializer, TicketFollowerUpdateSerializer, \
    TicketRevisionFilterSerializer, TicketRevisionUpdateSerializer, TicketSerializer, TicketUpdateSerializer, \
    TicketFilterSerializer
from acl.privilege import CozentusPermission
from django.core.paginator import Paginator
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from . import serializers
from rest_framework import serializers


class DepartmentListCreateView(generics.ListCreateAPIView):
    queryset = Department.objects.filter(is_active=True, is_delete=False)
    serializer_class = DepartmentSerializer


class DepartmentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Department.objects.filter(is_active=True, is_delete=False)
    serializer_class = DepartmentSerializer


class SLACreate(generics.ListCreateAPIView):
    # permission_classes = [CozentusPermission]

    serializer_class = SLASerializer
    queryset = SLA.objects.filter(is_delete=False)


class SLARetrieveUpdateDelete(RetrieveUpdateDestroyAPIView):
    # permission_classes = [CozentusPermission]

    serializer_class = SLAUpdateSerializer
    queryset = SLA.objects.all()


class StatusCreateApi(CreateAPIView):
    """
    This view class is used to Create a new Status
    """
    # permission_classes = (CozentusPermission,)
    serializer_class = StatusSerializer
    queryset = Status.objects.all()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user.id)


class StatusUpdateApi(RetrieveUpdateDestroyAPIView):
    """
    This view class is used to update an existing status
    """
    # permission_classes = (CozentusPermission,)
    serializer_class = StatusSerializer
    queryset = Status.objects.all()

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user.id)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance:
            instance.delete()
            return Response({"message": "Status deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"message": "Record not found."}, status=status.HTTP_404_NOT_FOUND)


class StatusFilterApi(APIView):
    """
    This view class is used to return status data with filter and pagination
    """
    # permission_classes = (CozentusPermission,)
    serializer_class = StatusSerializer

    @swagger_auto_schema(request_body=StatusReadSerializer)
    def post(self, request):
        """
        This method is used for retrieving status data with pagination and filter
        """
        try:
            page_size = request.data.get("page_size", 200)
            page = request.data.get("page", 1)
            if page < 1 or page_size < 1:
                return Response({"message": "page and page size should be positive integer"},
                                status=status.HTTP_400_BAD_REQUEST)
            status_name = request.data.get('name')
            status_code = request.data.get('status_code')
            order_by = request.data.get('order_by')
            order_type = request.data.get('order_type')
            # Perform filtering based on the provided parameters
            queryset = Status.objects.all()
            if status_name:
                queryset = queryset.filter(status_name__icontains=status_name)

            if status_code:
                queryset = queryset.filter(status_code=status_code)
            if order_by in ["status_name", "status_code"]:
                if order_type == "desc":
                    order_by = f"-{order_by}"
                queryset = queryset.order_by(order_by)
            # if request.data.get("export"):
            #     results = StatusReadSerializer(queryset, many=True)
            #     return export_query_to_excel(data=results.data, module_name="STATUS_DATA")
            # Create Paginator object with page_size objects per page
            paginator = Paginator(queryset, page_size)
            number_pages = paginator.num_pages
            if page > number_pages:
                return Response({"message": "Page not found"}, status=status.HTTP_400_BAD_REQUEST)
            # Get the page object for the requested page number
            page_obj = paginator.get_page(page)
            serializer = StatusFilterSerializer(page_obj, many=True)
            return Response({"count": len(queryset), "results": serializer.data})
        # except serializers.ValidationError as ve:
        #     raise serializers.ValidationError(ve.detail)
        except Exception as ee:
            return Response({"message": "Please provide valid data"}, status=status.HTTP_400_BAD_REQUEST)


class CategoryFilterApi(APIView):
    """
    This view class is used to return category data with filter and pagination
    """
    # permission_classes = (CozentusPermission,)
    serializer_class = CategoryFilterSerializer

    @swagger_auto_schema(request_body=CategoryFilterSerializer)
    def post(self, request):
        """
        This method is used for retrieving category data with pagination and filter
        """
        try:
            page_size = request.data.get("page_size", 200)
            page = request.data.get("page", 1)
            if page < 1 or page_size < 1:
                return Response({"message": "page and page size should be positive integer"},
                                status=status.HTTP_400_BAD_REQUEST)
            category_name = request.data.get('category_name')
            order_by = request.data.get('order_by')
            order_type = request.data.get('order_type')
            # Perform filtering based on the provided parameters
            if category_name:
                categories = Category.objects.filter(name__icontains=category_name)
            else:
                categories = Category.objects.all()

            if order_by in ["name"]:
                if order_type == "desc":
                    order_by = f"-{order_by}"
                categories = categories.order_by(order_by)

            # if request.data.get("export"):
            #     category_results = CategoryReadSerializer(categories, many=True)
            #     return export_query_to_excel(data=category_results.data, module_name="CATEGORY_DATA")

            # Create Paginator object with page_size objects per page
            category_paginator = Paginator(categories, page_size)
            category_number_pages = category_paginator.num_pages

            if page > category_number_pages:
                return Response({"message": "Page not found"}, status=status.HTTP_400_BAD_REQUEST)

            # Get the page object for the requested page number
            category_page_obj = category_paginator.get_page(page)
            category_serializer = CategoryFilterSerializer(category_page_obj, many=True)

            return Response({'count': categories.count(), 'results': category_serializer.data},
                            status=status.HTTP_200_OK)
        except serializers.ValidationError as ve:
            raise serializers.ValidationError(ve.detail)
        except Exception as ee:
            return serializers.ValidationError("Please provide valid data")


class CategoryCreateApi(CreateAPIView):
    """
    This view class is used to Create a new category
    """
    # permission_classes = (CozentusPermission,)
    # cozentus_object_permissions = {
    #     'GET': (permission_department_list,),
    #     'POST': (permission_department_create,)
    # }
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user.id)


class CategoryUpdateApi(RetrieveUpdateDestroyAPIView):
    """
    This view class is used to update an existing category
    """
    # cozentus_object_permissions = {
    #     'GET': (permission_department_view,),
    #     # 'PUT': (permission_department_update,),
    #     # 'PATCH': (permission_department_update,),
    #     'DELETE': (permission_department_delete,)
    #
    # }
    # permission_classes = (CozentusPermission,)
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    def perform_update(self, serializer):
        serializer.save(modified_by=self.request.user.id)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance:
            instance.delete()
            return Response({"message": "Category deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"message": "Record not found."}, status=status.HTTP_404_NOT_FOUND)


class ProjectCreateApi(CreateAPIView):
    """
    Code list create and get api
    """

    serializer_class = ProjectManagementSerializer
    queryset = ProjectManagement.objects.all()

    # ToDo user to be added later, as of now hardcoded
    def perform_create(self, serializer):
        serializer.save(created_by=15)


class ProjectRetrieveUpdateDeleteApi(RetrieveUpdateDestroyAPIView):
    """
    Code list update and delete api
    """

    serializer_class = ProjectManagementSerializer
    queryset = ProjectManagement.objects.all()

    def perform_update(self, serializer):
        serializer.save(modified_by=15,
                        modified_on=timezone.now().astimezone(timezone.timezone.utc))

    def perform_destroy(self, instance):
        instance.deleted_at = timezone.now().astimezone(timezone.timezone.utc)
        instance.save()


class ProjectFilterApi(APIView):
    serializer_class = ProjectManagementReadSerializer

    @swagger_auto_schema(request_body=ProjectFilterSerializers)
    def post(self, request):
        """
        This method is used for retrieving role permission data with pagination and filter
        """
        try:
            page_size = request.data.get("page_size", 50)
            page = request.data.get("page", 1)
            if page < 1 or page_size < 1:
                return Response({"message": "page and page size should be positive integer"},
                                status=status.HTTP_400_BAD_REQUEST)
            order_by = request.data.get('order_by')
            order_type = request.data.get('order_type')
            serializer = ProjectFilterSerializers(data=request.data)
            serializer.is_valid(raise_exception=True)
            data = serializer.data
            filter_dict = {
                "id": "id", "client_id": "client_id",
                "client_name": "client_name__icontains",
                "department_id": "department_id", "project_id": "project_id", "project_name": "project_name__icontains",
                "contact_name": "contact_name__icontains",
                "project_manager_primary": "project_manager_primary__icontains",
                "support_group_email": "support_group_email__icontains", "product_owner": "product_owner__icontains",
                "contact_email": "contact_email__icontains", "is_active": "is_active__icontains",
                "created_at": "created_at", "created_by": "created_by",
                "updated_at": "updated_at", "updated_by": "updated_by"
            }
            query_dict = {filter_dict.get(key, None): value for key, value in data.items() if
                          value or isinstance(value, (int, bool))}
            query_dict = {key: value for key, value in query_dict.items() if key}
            queryset = ProjectManagement.objects.filter(**query_dict).order_by('-created_at')
            order_dict = {
                "id": "id", "client_id": "client_id",
                "client_name": "client_name",
                "department_id": "department_id", "project_id": "project_id", "project_name": "project_name",
                "contact_name": "contact_name",
                "project_manager_primary": "project_manager_primary",
                "support_group_email": "support_group_email", "product_owner": "product_owner",
                "contact_email": "contact_email", "is_active": "is_active",
                "created_at": "created_at", "created_by": "created_by",
                "updated_at": "updated_at", "updated_by": "updated_by"
            }
            query_filter = order_dict.get(order_by, None)
            if query_filter:
                if order_type == "desc":
                    query_filter = f"-{query_filter}"
                queryset = queryset.order_by(query_filter)
            # if data.get("export"):
            #     result = self.serializer_class(queryset, many=True)
            #     return export_query_to_excel(result.data, module_name="CODELIST_LIBRARY")
            paginator = Paginator(queryset, page_size)
            number_pages = paginator.num_pages
            if page > number_pages:
                return Response({"message": "Page not found"}, status=status.HTTP_400_BAD_REQUEST)
            # Get the page object for the requested page number
            page_obj = paginator.get_page(page)
            serializer = self.serializer_class(page_obj, many=True)
            data = serializer.data
            return Response({"count": queryset.count(), "results": data})

        except ValueError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ee:
            return Response(str(ee), status=status.HTTP_400_BAD_REQUEST)


class DepartmentFilterApi(APIView):
    """
    This view class is used to return department data with filter and pagination
    """
    serializer_class = DepartmentFilterSerializer
    cozentus_object_permissions = {
        # 'GET': (permission_department_view,),
        # 'PUT': (permission_department_update,),
        # 'PATCH': (permission_department_update,),
        # 'DELETE': (permission_department_delete,)

    }

    @swagger_auto_schema(request_body=DepartmentSerializer)
    def post(self, request):
        """
        This method is used to make post request for pagination and filter and return the department data.
        """
        try:
            order_by = request.data.pop('order_by', None)
            order_type = request.data.pop('order_type', None)
            page_size = request.data.get("page_size", 50)
            page = request.data.get("page", 1)

            if page < 1 or page_size < 1:
                return Response({"message": "page and page size should be positive integer"},
                                status=status.HTTP_400_BAD_REQUEST)

            serializer = DepartmentFilterSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            data = serializer.validated_data

            filter_dict = {
                "department_name": "department_name__icontains",
                "department_code": "department_code__icontains",
                "department_type": "department_type"
            }

            query_filter = {filter_dict[key]: value for key, value in data.items() if value}

            departments = Department.objects.filter(**query_filter)

            order_by_dict = {
                "department_name": "department_name",
                "department_code": "department_code",
                "department_type": "department_type",
            }

            query_order_by = order_by_dict.get(order_by)

            if order_type == "desc" and query_order_by:
                query_order_by = f"-{query_order_by}"

            if query_order_by:
                departments = departments.order_by(query_order_by)

            # if data.get("export"):
            #     results = DepartmentSerializer(departments, many=True)
            #     return export_query_to_excel(data=results.data, module_name="DEPARTMENT_MANAGEMENT")

            # Create Paginator object with page_size objects per page
            paginator = Paginator(departments, page_size)
            number_pages = paginator.num_pages

            if page > number_pages and page > 1:
                return Response({"message": "Page not found"}, status=status.HTTP_400_BAD_REQUEST)

            # Get the page object for the requested page number
            page_obj = paginator.get_page(page)
            results = DepartmentFilterSerializer(page_obj, many=True)

            return Response({'count': departments.count(), 'results': results.data}, status=status.HTTP_200_OK)

        # except FieldError as fe:
        #     return Response({"message": str(fe)}, status=status.HTTP_400_BAD_REQUEST)

        except serializers.ValidationError as ve:
            raise serializers.ValidationError(ve.detail)

        except Exception as ee:
            return Response(str(ee), status=status.HTTP_400_BAD_REQUEST)


class DepartmentCreateApi(CreateAPIView):
    """
    This view class is used to Create a new department
    """
    # permission_classes = (CozentusPermission,)
    serializer_class = DepartmentSerializer
    queryset = Department.objects.all()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user.id)


class DepartmentUpdateApi(RetrieveUpdateDestroyAPIView):
    """
    This view class is used to update an existing department
    """
    # permission_classes = (CozentusPermission,)
    serializer_class = DepartmentSerializer
    queryset = Department.objects.all()

    def perform_update(self, serializer):
        serializer.save(modified_by=self.request.user.id)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance:
            instance.delete()
            return Response({"message": "Department deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"message": "Record not found."}, status=status.HTTP_404_NOT_FOUND)


class TicketTypeCreateAPI(generics.ListCreateAPIView):
    # permission_classes = [CozentusPermission]

    serializer_class = TicketTypeSerializer
    queryset = TicketType.objects.all()


class TicketTypeUpdateAPI(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = [CozentusPermission]

    serializer_class = TicketTypeUpdateSerializer
    queryset = TicketType.objects.all()


class TicketFollowerCreateAPI(generics.CreateAPIView):
    queryset = TicketFollower.objects.filter(deleted_at__isnull=True)
    serializer_class = TicketFollowerSerializer


class TicketFollowerFilterAPI(APIView):
    serializer_class = TicketFollowerFilterSerializer

    @swagger_auto_schema(request_body=TicketFollowerFilterSerializer)
    def post(self, request):
        """
        Retrieve ticket follower data with pagination and filter
        """
        try:
            per_page = request.data.get("per_page", 50)
            page = request.data.get("page", 1)
            if page < 1 or per_page < 1:
                return Response({"message": "page and page size should be positive integer"},
                                status=status.HTTP_400_BAD_REQUEST)

            order_by = request.data.get('order_by')
            order_type = request.data.get('order_type')
            serializer = TicketFollowerFilterSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            data = serializer.data
            filter_dict = {
                "ticket_id": "ticket_id", "follower_id": "follower_id",
                "created_at": "created_at", "created_by": "created_by",
                "updated_at": "updated_at", "updated_by": "updated_by"
            }
            query_dict = {filter_dict.get(key, None): value for key, value in data.items() if
                          value or isinstance(value, (int, bool))}
            query_dict = {key: value for key, value in query_dict.items() if key}
            queryset = TicketFollower.objects.filter(**query_dict)
            order_dict = {
                "ticket_id": "ticket_id", "follower_id": "follower_id",
                "created_at": "created_at", "created_by": "created_by",
                "updated_at": "updated_at", "updated_by": "updated_by"
            }
            query_filter = order_dict.get(order_by, None)
            if query_filter:
                if order_type == "desc":
                    query_filter = f"-{query_filter}"
                queryset = queryset.order_by(query_filter)
            paginator = Paginator(queryset, per_page)
            number_pages = paginator.num_pages
            if page > number_pages:
                return Response({"message": "Page not found"}, status=status.HTTP_400_BAD_REQUEST)
            page_obj = paginator.get_page(page)
            serializer = TicketFollowerSerializer(page_obj, many=True)
            data = serializer.data
            return Response({"count": queryset.count(), "results": data})

        except ValueError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ee:
            return Response({"message": str(ee)}, status=status.HTTP_400_BAD_REQUEST)


class TicketFollowerUpdateAPI(RetrieveUpdateDestroyAPIView):
    queryset = TicketFollower.objects.all()
    serializer_class = TicketFollowerUpdateSerializer


class TicketRevisionCreateAPI(CreateAPIView):
    queryset = TicketRevision.objects.filter(deleted_at__isnull=True)
    serializer_class = TicketRevisionSerializer


class TicketRevisionFilterAPI(APIView):
    serializer_class = TicketRevisionFilterSerializer

    @swagger_auto_schema(request_body=TicketRevisionFilterSerializer)
    def post(self, request):
        """
        Retrieve ticket revision data with pagination and filter
        """
        try:
            per_page = request.data.get("per_page", 50)
            page = request.data.get("page", 1)
            if page < 1 or per_page < 1:
                return Response({"message": "page and page size should be positive integer"},
                                status=status.HTTP_400_BAD_REQUEST)

            order_by = request.data.get('order_by')
            order_type = request.data.get('order_type')
            serializer = TicketRevisionFilterSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            data = serializer.data
            filter_dict = {
                "ticket_id": "ticket_id", "revision_status": "revision_status",
                "pti": "pti", "action_taken": "action_taken",
                "before_revision": "before_revision", "after_revision": "after_revision",
                "created_at": "created_at", "created_by": "created_by",
                "updated_at": "updated_at", "updated_by": "updated_by"
            }
            query_dict = {filter_dict.get(key, None): value for key, value in data.items() if
                          value or isinstance(value, (int, bool))}
            query_dict = {key: value for key, value in query_dict.items() if key}
            queryset = TicketRevision.objects.filter(**query_dict)
            order_dict = {
                "ticket_id": "ticket_id", "revision_status": "revision_status",
                "pti": "pti", "action_taken": "action_taken",
                "before_revision": "before_revision", "after_revision": "after_revision",
                "created_at": "created_at", "created_by": "created_by",
                "updated_at": "updated_at", "updated_by": "updated_by"
            }
            query_filter = order_dict.get(order_by, None)
            if query_filter:
                if order_type == "desc":
                    query_filter = f"-{query_filter}"
                queryset = queryset.order_by(query_filter)
            paginator = Paginator(queryset, per_page)
            number_pages = paginator.num_pages
            if page > number_pages:
                return Response({"message": "Page not found"}, status=status.HTTP_400_BAD_REQUEST)
            page_obj = paginator.get_page(page)
            serializer = TicketRevisionSerializer(page_obj, many=True)
            data = serializer.data
            return Response({"count": queryset.count(), "results": data})

        except ValueError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ee:
            return Response({"message": str(ee)}, status=status.HTTP_400_BAD_REQUEST)


class TicketRevisionUpdateAPI(RetrieveUpdateDestroyAPIView):
    queryset = TicketRevision.objects.all()
    serializer_class = TicketRevisionUpdateSerializer


class TicketCreateAPI(CreateAPIView):
    queryset = Ticket.objects.filter(is_delete=False)
    serializer_class = TicketSerializer


class TicketFilterAPI(APIView):
    serializer_class = TicketFilterSerializer

    @swagger_auto_schema(request_body=TicketFilterSerializer)
    def post(self, request):
        """
        Retrieve ticket data with pagination and filter
        """
        try:
            per_page = request.data.get("per_page", 50)
            page = request.data.get("page", 1)
            if page < 1 or per_page < 1:
                return Response({"message": "page and page size should be positive integer"},
                                status=status.HTTP_400_BAD_REQUEST)

            order_by = request.data.get('order_by')
            order_type = request.data.get('order_type')
            serializer = TicketFilterSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            data = serializer.data
            filter_dict = {
                "ticket_no": "ticket_no__icontains", "ticket_status": "ticket_status",
                "ticket_category": "ticket_category", "ticket_type": "ticket_type",
                "department_id": "department_id", "project_id": "project_id",
                "ticket_priority": "ticket_priority", "created_at": "created_at",
                "created_by": "created_by", "updated_at": "updated_at", "updated_by": "updated_by"
            }
            query_dict = {filter_dict.get(key, None): value for key, value in data.items() if
                          value or isinstance(value, (int, bool))}
            query_dict = {key: value for key, value in query_dict.items() if key}
            queryset = Ticket.objects.filter(**query_dict)
            order_dict = {
                "ticket_no": "ticket_no", "ticket_status": "ticket_status",
                "ticket_category": "ticket_category", "ticket_type": "ticket_type",
                "department_id": "department_id", "project_id": "project_id",
                "ticket_priority": "ticket_priority", "created_at": "created_at",
                "created_by": "created_by", "updated_at": "updated_at", "updated_by": "updated_by"
            }
            query_filter = order_dict.get(order_by, None)
            if query_filter:
                if order_type == "desc":
                    query_filter = f"-{query_filter}"
                queryset = queryset.order_by(query_filter)
            paginator = Paginator(queryset, per_page)
            number_pages = paginator.num_pages
            if page > number_pages:
                return Response({"message": "Page not found"}, status=status.HTTP_400_BAD_REQUEST)
            page_obj = paginator.get_page(page)
            serializer = TicketSerializer(page_obj, many=True)
            data = serializer.data
            return Response({"count": queryset.count(), "results": data})

        except ValueError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ee:
            return Response({"message": str(ee)}, status=status.HTTP_400_BAD_REQUEST)


class TicketUpdateAPI(RetrieveUpdateDestroyAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketUpdateSerializer
