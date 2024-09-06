from case_management.utility import log_activity
from .models import SLA
# from .permissions import permission_sla_edit, permission_sla_view, permission_sla_create
from .serializers import SLASerializer, SLAUpdateSerializer, SLAFilterSerializer, \
    SLAReadSerializer
from acl.privilege import CozentusPermission
from django.core.paginator import Paginator
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from . import serializers
from rest_framework import serializers
from drf_spectacular.utils import extend_schema
import logging

logger = logging.getLogger(__name__)


# class DepartmentListCreateView(generics.ListCreateAPIView):
#     permission_classes = [CozentusPermission]

#
# class LargeResultsSetPagination(PageNumberPagination):
#     page_size = 1000
#     page_size_query_param = 'page_size'
#     max_page_size = 10000
#
#
# class ProjectCreateApi(CreateAPIView):
#     """
#     Code list create and get api
#     """
#     permission_classes = (CozentusPermission,)
#     serializer_class = ProjectManagementSerializer
#     queryset = ProjectManagement.objects.all()
#
# ToDo user to be added later, as of now hardcoded
#     def perform_create(self, serializer):
#         serializer.save(created_by=15)
#
#
# class ProjectRetrieveUpdateDeleteApi(RetrieveUpdateDestroyAPIView):
#     """
#     Code list update and delete api
#     """
#     permission_classes = (CozentusPermission,)
#     serializer_class = ProjectManagementSerializer
#     queryset = ProjectManagement.objects.all()
#
#     def perform_update(self, serializer):
#         serializer.save(modified_by=15,
#                         modified_on=timezone.now().astimezone(timezone.timezone.utc))
#
#     def perform_destroy(self, instance):
#         instance.deleted_at = timezone.now().astimezone(timezone.timezone.utc)
#         instance.save()
#
#
# class ProjectFilterApi(APIView):
#     serializer_class = ProjectManagementReadSerializer
#     permission_classes = (CozentusPermission,)
#
#     # @swagger_auto_schema(request_body=ProjectFilterSerializers)
#     @extend_schema(request=ProjectFilterSerializers, responses=ProjectManagementReadSerializer)
#     def post(self, request):
#         """
#         This method is used for retrieving role permission data with pagination and filter
#         """
#         try:
#             page_size = request.data.get("page_size", 50)
#             page = request.data.get("page", 1)
#             if page < 1 or page_size < 1:
#                 return Response({"message": "page and page size should be positive integer"},
#                                 status=status.HTTP_400_BAD_REQUEST)
#             order_by = request.data.get('order_by')
#             order_type = request.data.get('order_type')
#             serializer = ProjectFilterSerializers(data=request.data)
#             serializer.is_valid(raise_exception=True)
#             data = serializer.data
#             filter_dict = {
#                 "id": "id", "client_id": "client_id",
#                 "client_name": "client_name__icontains",
#                 "department_id": "department_id", "project_id": "project_id", "project_name": "project_name__icontains",
#                 "contact_name": "contact_name__icontains",
#                 "project_manager_primary": "project_manager_primary__icontains",
#                 "support_group_email": "support_group_email__icontains", "product_owner": "product_owner__icontains",
#                 "contact_email": "contact_email__icontains", "is_active": "is_active__icontains",
#                 "created_on": "created_on", "created_by": "created_by",
#                 "modified_on": "modified_on", "modified_by": "modified_by"
#             }
#             query_dict = {filter_dict.get(key, None): value for key, value in data.items() if
#                           value or isinstance(value, (int, bool))}
#             query_dict = {key: value for key, value in query_dict.items() if key}
#             queryset = ProjectManagement.objects.filter(**query_dict).order_by('-created_on')
#             order_dict = {
#                 "id": "id", "client_id": "client_id",
#                 "client_name": "client_name",
#                 "department_id": "department_id", "project_id": "project_id", "project_name": "project_name",
#                 "contact_name": "contact_name",
#                 "project_manager_primary": "project_manager_primary",
#                 "support_group_email": "support_group_email", "product_owner": "product_owner",
#                 "contact_email": "contact_email", "is_active": "is_active",
#                 "created_on": "created_on", "created_by": "created_by",
#                 "modified_on": "modified_on", "modified_by": "modified_by"
#             }
#             query_filter = order_dict.get(order_by, None)
#             if query_filter:
#                 if order_type == "desc":
#                     query_filter = "-%s" % query_filter
#                 queryset = queryset.order_by(query_filter)
#             # if data.get("export"):
#             #     result = self.serializer_class(queryset, many=True)
#             #     return export_query_to_excel(result.data, module_name="CODELIST_LIBRARY")
#             paginator = Paginator(queryset, page_size)
#             number_pages = paginator.num_pages
#             if page > number_pages:
#                 return Response({"message": "Page not found"}, status=status.HTTP_400_BAD_REQUEST)
#             # Get the page object for the requested page number
#             page_obj = paginator.get_page(page)
#             serializer = self.serializer_class(page_obj, many=True)
#             data = serializer.data
#             return Response({"count": queryset.count(), "results": data})
#
#         except ValueError as e:
#             return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
#         except Exception as ee:
#             return Response(str(ee), status=status.HTTP_400_BAD_REQUEST)
#
#
# class TicketTypeCreateAPI(generics.CreateAPIView):
#     permission_classes = [CozentusPermission]
#
#     serializer_class = TicketTypeSerializer
#     queryset = TicketType.objects.all()
#
#     def perform_create(self, serializer):
#         serializer.save(created_by=self.request.user.id)
#
#
# class TicketTypeUpdateAPI(generics.RetrieveUpdateDestroyAPIView):
#     permission_classes = [CozentusPermission]
#
#     serializer_class = TicketTypeUpdateSerializer
#     queryset = TicketType.objects.all()
#
#
# class TicketFollowerCreateAPI(generics.CreateAPIView):
#     permission_classes = [CozentusPermission]
#     queryset = TicketFollower.objects.filter(deleted_at__isnull=True)
#     serializer_class = TicketFollowerSerializer
#
#
# class TicketFollowerFilterAPI(APIView):
#     permission_classes = [CozentusPermission]
#     serializer_class = TicketFollowerFilterSerializer
#
#     @swagger_auto_schema(request_body=TicketFollowerFilterSerializer)
#     def post(self, request):
#         """
#         Retrieve ticket follower data with pagination and filter
#         """
#         try:
#             per_page = request.data.get("per_page", 50)
#             page = request.data.get("page", 1)
#             if page < 1 or per_page < 1:
#                 return Response({"message": "page and page size should be positive integer"},
#                                 status=status.HTTP_400_BAD_REQUEST)
#
#             order_by = request.data.get('order_by')
#             order_type = request.data.get('order_type')
#             serializer = TicketFollowerFilterSerializer(data=request.data)
#             serializer.is_valid(raise_exception=True)
#             data = serializer.data
#             filter_dict = {
#                 "ticket_id": "ticket_id", "follower_id": "follower_id",
#                 "created_on": "created_on", "created_by": "created_by",
#                 "modified_on": "modified_on", "modified_by": "modified_by"
#             }
#             query_dict = {filter_dict.get(key, None): value for key, value in data.items() if
#                           value or isinstance(value, (int, bool))}
#             query_dict = {key: value for key, value in query_dict.items() if key}
#             queryset = TicketFollower.objects.filter(**query_dict)
#             order_dict = {
#                 "ticket_id": "ticket_id", "follower_id": "follower_id",
#                 "created_on": "created_on", "created_by": "created_by",
#                 "modified_on": "modified_on", "modified_by": "modified_by"
#             }
#             query_filter = order_dict.get(order_by, None)
#             if query_filter:
#                 if order_type == "desc":
#                     query_filter = "-%s" % query_filter
#                 queryset = queryset.order_by(query_filter)
#             paginator = Paginator(queryset, per_page)
#             number_pages = paginator.num_pages
#             if page > number_pages:
#                 return Response({"message": "Page not found"}, status=status.HTTP_400_BAD_REQUEST)
#             page_obj = paginator.get_page(page)
#             serializer = TicketFollowerSerializer(page_obj, many=True)
#             data = serializer.data
#             return Response({"count": queryset.count(), "results": data})
#
#         except ValueError as e:
#             return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
#         except Exception as ee:
#             return Response({"message": str(ee)}, status=status.HTTP_400_BAD_REQUEST)
#
#
# class TicketFollowerUpdateAPI(RetrieveUpdateDestroyAPIView):
#     permission_classes = [CozentusPermission]
#     queryset = TicketFollower.objects.all()
#     serializer_class = TicketFollowerUpdateSerializer
#
#
# class TicketRevisionCreateAPI(CreateAPIView):
#     permission_classes = [CozentusPermission]
#     queryset = TicketRevision.objects.filter(deleted_at__isnull=True)
#     serializer_class = TicketRevisionSerializer
#
#
# class TicketRevisionFilterAPI(APIView):
#     serializer_class = TicketRevisionFilterSerializer
#     permission_classes = [CozentusPermission]
#
#     @swagger_auto_schema(request_body=TicketRevisionFilterSerializer)
#     def post(self, request):
#         """
#         Retrieve ticket revision data with pagination and filter
#         """
#         try:
#             per_page = request.data.get("per_page", 50)
#             page = request.data.get("page", 1)
#             if page < 1 or per_page < 1:
#                 return Response({"message": "page and page size should be positive integer"},
#                                 status=status.HTTP_400_BAD_REQUEST)
#
#             order_by = request.data.get('order_by')
#             order_type = request.data.get('order_type')
#             serializer = TicketRevisionFilterSerializer(data=request.data)
#             serializer.is_valid(raise_exception=True)
#             data = serializer.data
#             filter_dict = {
#                 "ticket_id": "ticket_id", "revision_status": "revision_status",
#                 "pti": "pti", "action_taken": "action_taken",
#                 "before_revision": "before_revision", "after_revision": "after_revision",
#                 "created_on": "created_on", "created_by": "created_by",
#                 "modified_on": "modified_on", "modified_by": "modified_by"
#             }
#             query_dict = {filter_dict.get(key, None): value for key, value in data.items() if
#                           value or isinstance(value, (int, bool))}
#             query_dict = {key: value for key, value in query_dict.items() if key}
#             queryset = TicketRevision.objects.filter(**query_dict)
#             order_dict = {
#                 "ticket_id": "ticket_id", "revision_status": "revision_status",
#                 "pti": "pti", "action_taken": "action_taken",
#                 "before_revision": "before_revision", "after_revision": "after_revision",
#                 "created_on": "created_on", "created_by": "created_by",
#                 "modified_on": "modified_on", "modified_by": "modified_by"
#             }
#             query_filter = order_dict.get(order_by, None)
#             if query_filter:
#                 if order_type == "desc":
#                     query_filter = "-%s" % query_filter
#                 queryset = queryset.order_by(query_filter)
#             paginator = Paginator(queryset, per_page)
#             number_pages = paginator.num_pages
#             if page > number_pages:
#                 return Response({"message": "Page not found"}, status=status.HTTP_400_BAD_REQUEST)
#             page_obj = paginator.get_page(page)
#             serializer = TicketRevisionSerializer(page_obj, many=True)
#             data = serializer.data
#             return Response({"count": queryset.count(), "results": data})
#
#         except ValueError as e:
#             return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
#         except Exception as ee:
#             return Response({"message": str(ee)}, status=status.HTTP_400_BAD_REQUEST)
#
#
# class TicketRevisionUpdateAPI(RetrieveUpdateDestroyAPIView):
#     permission_classes = [CozentusPermission]
#     queryset = TicketRevision.objects.all()
#     serializer_class = TicketRevisionUpdateSerializer
#
#
# class TicketCreateAPI(CreateAPIView):
#     permission_classes = [CozentusPermission]
#     queryset = Ticket.objects.filter(is_delete=False)
#     serializer_class = TicketSerializer
#
#
# class TicketFilterAPI(APIView):
#     serializer_class = TicketFilterSerializer
#     permission_classes = [CozentusPermission]
#
#     @swagger_auto_schema(request_body=TicketFilterSerializer)
#     def post(self, request):
#         """
#         Retrieve ticket data with pagination and filter
#         """
#         try:
#             per_page = request.data.get("per_page", 50)
#             page = request.data.get("page", 1)
#             if page < 1 or per_page < 1:
#                 return Response({"message": "page and page size should be positive integer"},
#                                 status=status.HTTP_400_BAD_REQUEST)
#
#             order_by = request.data.get('order_by')
#             order_type = request.data.get('order_type')
#             serializer = TicketFilterSerializer(data=request.data)
#             serializer.is_valid(raise_exception=True)
#             data = serializer.data
#             filter_dict = {
#                 "ticket_no": "ticket_no__icontains", "ticket_status": "ticket_status",
#                 "ticket_category": "ticket_category", "ticket_type": "ticket_type",
#                 "department_id": "department_id", "project_id": "project_id",
#                 "ticket_priority": "ticket_priority", "created_on": "created_on",
#                 "created_by": "created_by", "modified_on": "modified_on", "modified_by": "modified_by"
#             }
#             query_dict = {filter_dict.get(key, None): value for key, value in data.items() if
#                           value or isinstance(value, (int, bool))}
#             query_dict = {key: value for key, value in query_dict.items() if key}
#             queryset = Ticket.objects.filter(**query_dict)
#             order_dict = {
#                 "ticket_no": "ticket_no", "ticket_status": "ticket_status",
#                 "ticket_category": "ticket_category", "ticket_type": "ticket_type",
#                 "department_id": "department_id", "project_id": "project_id",
#                 "ticket_priority": "ticket_priority", "created_on": "created_on",
#                 "created_by": "created_by", "modified_on": "modified_on", "modified_by": "modified_by"
#             }
#             query_filter = order_dict.get(order_by, None)
#             if query_filter:
#                 if order_type == "desc":
#                     query_filter = "-%s" % query_filter
#                 queryset = queryset.order_by(query_filter)
#             paginator = Paginator(queryset, per_page)
#             number_pages = paginator.num_pages
#             if page > number_pages:
#                 return Response({"message": "Page not found"}, status=status.HTTP_400_BAD_REQUEST)
#             page_obj = paginator.get_page(page)
#             serializer = TicketSerializer(page_obj, many=True)
#             data = serializer.data
#             return Response({"count": queryset.count(), "results": data})
#
#         except ValueError as e:
#             return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
#         except Exception as ee:
#             return Response({"message": str(ee)}, status=status.HTTP_400_BAD_REQUEST)
#
#
# class TicketUpdateAPI(RetrieveUpdateDestroyAPIView):
#     permission_classes = [CozentusPermission]
#     queryset = Ticket.objects.all()
#     serializer_class = TicketUpdateSerializer
#
#
# class TicketBehalfCreateAPI(CreateAPIView):
#     permission_classes = [CozentusPermission]
#     queryset = TicketBehalf.objects.filter(deleted_at__isnull=True)
#     serializer_class = TicketBehalfSerializer
#
#
# class TicketBehalfFilterAPI(APIView):
#     permission_classes = [CozentusPermission]
#     serializer_class = TicketBehalfFilterSerializer
#
#     @swagger_auto_schema(request_body=TicketBehalfFilterSerializer)
#     def post(self, request):
#         """
#         Retrieve ticket behalf data with pagination and filter
#         """
#         try:
#             per_page = request.data.get("per_page", 50)
#             page = request.data.get("page", 1)
#             if page < 1 or per_page < 1:
#                 return Response({"message": "page and page size should be positive integer"},
#                                 status=status.HTTP_400_BAD_REQUEST)
#
#             order_by = request.data.get('order_by')
#             order_type = request.data.get('order_type')
#             serializer = TicketBehalfFilterSerializer(data=request.data)
#             serializer.is_valid(raise_exception=True)
#             data = serializer.data
#             filter_dict = {
#                 "ticket_id": "ticket_id", "behalf_email": "behalf_email",
#                 "created_on": "created_on", "created_by": "created_by",
#                 "modified_on": "modified_on", "modified_by": "modified_by"
#             }
#             query_dict = {filter_dict.get(key, None): value for key, value in data.items() if
#                           value or isinstance(value, (int, bool))}
#             query_dict = {key: value for key, value in query_dict.items() if key}
#             queryset = TicketBehalf.objects.filter(**query_dict)
#             order_dict = {
#                 "ticket_id": "ticket_id", "behalf_email": "behalf_email",
#                 "created_on": "created_on", "created_by": "created_by",
#                 "modified_on": "modified_on", "modified_by": "modified_by"
#             }
#             query_filter = order_dict.get(order_by, None)
#             if query_filter:
#                 if order_type == "desc":
#                     query_filter = "-%s" % query_filter
#                 queryset = queryset.order_by(query_filter)
#             paginator = Paginator(queryset, per_page)
#             number_pages = paginator.num_pages
#             if page > number_pages:
#                 return Response({"message": "Page not found"}, status=status.HTTP_400_BAD_REQUEST)
#             page_obj = paginator.get_page(page)
#             serializer = TicketBehalfSerializer(page_obj, many=True)
#             data = serializer.data
#             return Response({"count": queryset.count(), "results": data})
#
#         except ValueError as e:
#             return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
#         except Exception as ee:
#             return Response({"message": str(ee)}, status=status.HTTP_400_BAD_REQUEST)
#
#
# class TicketBehalfUpdateAPI(RetrieveUpdateDestroyAPIView):
#     permission_classes = [CozentusPermission]
#     queryset = TicketBehalf.objects.all()
#     serializer_class = TicketBehalfUpdateSerializer
#
#
# class PriorityListCreateApi(ListCreateAPIView):
#     queryset = Priority.objects.all()
#     serializer_class = PrioritySerializer
#     # case_management_object_permissions = {
#     #     'POST': (permission_priority_create,),
#     #     'GET': (permission_priority_view,)
#     # }
#     permission_classes = (CozentusPermission,)
#
#
# class PriorityModifyApi(RetrieveUpdateDestroyAPIView):
#     queryset = Priority.objects.all()
#     serializer_class = PrioritySerializer
#     case_management_object_permissions = {
#         'PUT': (permission_priority_edit,),
#         'PATCH': (permission_priority_edit,),
#         'DELETE': (permission_priority_delete,)
#     }
#     permission_classes = (CozentusPermission,)
#
#
# class TicketTypeFilterApi(APIView):
#     permission_classes = (CozentusPermission,)
#     case_management_object_permissions = {
#         'POST': (permission_ticket_type_create,),  # Replace with actual permissions
#     }
#
#     # @swagger_auto_schema(request_body=TicketTypeFilterSerializer)
#     @extend_schema(request=TicketTypeFilterSerializer, responses=TicketTypeReadSerializer)
#     def post(self, request):
#         """
#         This method is used to make a POST request for pagination, filtering, and returning TicketType data.
#         """
#         try:
#             order_by = request.data.pop('order_by', None)
#             order_type = request.data.pop('order_type', None)
#             page_size = request.data.get("page_size", 50)
#             page = request.data.get("page", 1)
#
#             if page < 1 or page_size < 1:
#                 return Response({"message": "Page and page size should be positive integers"},
#                                 status=status.HTTP_400_BAD_REQUEST)
#
#             serializer = TicketTypeFilterSerializer(data=request.data)
#             serializer.is_valid(raise_exception=True)
#             data = serializer.validated_data
#
#             filter_dict = {
#                 "name": "name__icontains",
#                 "is_active": "is_active",
#             }
#
#             # query_filter = {filter_dict.get(key): value for key, value in data.items() if value is not None}
#             query_filter = {filter_dict[key]: value for key, value in data.items() if
#                             key in filter_dict and value is not None}
#             ticket_types = TicketType.objects.filter(**query_filter)
#
#             order_by_dict = {
#                 "name": "name",
#                 "is_active": "is_active",
#             }
#
#             query_order_by = order_by_dict.get(order_by)
#
#             if order_type == "desc" and query_order_by:
#                 query_order_by = f"-{query_order_by}"
#
#             if query_order_by:
#                 ticket_types = ticket_types.order_by(query_order_by)
#
#             # Create Paginator object with page_size objects per page
#             paginator = Paginator(ticket_types, page_size)
#             number_pages = paginator.num_pages
#
#             if page > number_pages and page > 1:
#                 return Response({"message": "Page not found"}, status=status.HTTP_400_BAD_REQUEST)
#
#             # Get the page object for the requested page number
#             page_obj = paginator.get_page(page)
#             results = TicketTypeReadSerializer(page_obj, many=True)
#
#             return Response({'count': ticket_types.count(), 'results': results.data}, status=status.HTTP_200_OK)
#
#         except FieldError as fe:
#             return Response({"message": str(fe)}, status=status.HTTP_400_BAD_REQUEST)
#
#         except serializers.ValidationError as ve:
#             return Response({"message": str(ve)}, status=status.HTTP_400_BAD_REQUEST)
#
#         except Exception as ee:
#             return Response({"message": str(ee)}, status=status.HTTP_400_BAD_REQUEST)


class SLACreateApi(CreateAPIView):
    """
    SLA Create API view
    """
    # case_management_object_permissions = {
        # 'POST': (permission_sla_create,),
    # }
    permission_classes = [CozentusPermission]
    serializer_class = SLASerializer
    queryset = SLA.objects.filter(is_delete=False)

    def perform_create(self, serializer):
        try:
            instance = serializer.save(created_by=self.request.user.id)
            after_instance = SLA.objects.get(pk=instance.pk)
            log_activity(
                instance=instance,
                request=self.request,
                action_type='CREATE',
                before_instance=None,
                after_instance=after_instance,
                description="SLA Created",
            )
            logger.info(f'SLA created successfully: {instance.id}')
        except Exception as e:
            logger.error(f'Error creating SLA: {str(e)}', exc_info=True)


class SLARetrieveUpdateDelete(RetrieveUpdateDestroyAPIView):
    """
    SLA Retrieve, Update, and Delete API view
    """
    queryset = SLA.objects.all()
    serializer_class = SLAUpdateSerializer
    response_time = serializers.TimeField(format='%H:%M:%S', input_formats=['%H:%M:%S'])
    resolution_time = serializers.TimeField(format='%H:%M:%S', input_formats=['%H:%M:%S'])

    def perform_update(self, serializer):
        try:
            instance = self.get_object()
            before_instance = SLA.objects.get(pk=instance.pk)
            serializer.save(modified_by=self.request.user.id)
            after_instance = SLA.objects.get(pk=instance.pk)
            log_activity(
                instance=instance,
                request=self.request,
                action_type='UPDATE',
                before_instance=before_instance,
                after_instance=after_instance,
                description="SLA Updated",
            )
            logger.info(f'SLA updated successfully: {instance.id}')
        except Exception as e:
            logger.error(f'Error updating SLA: {str(e)}', exc_info=True)

    def perform_destroy(self, instance):
        try:
            before_instance = instance
            instance.is_delete = True
            instance.save()
            log_activity(
                instance=instance,
                request=self.request,
                action_type='DELETE',
                before_instance=before_instance,
                after_instance=None,  # No after_instance for soft delete
                description="SLA Marked as Deleted",
            )
            logger.info(f'SLA marked as deleted: {instance.id}')
        except Exception as e:
            logger.error(f'Error deleting SLA: {str(e)}', exc_info=True)


class SLAFilterApi(APIView):
    """
    SLA Filter API to retrieve filtered and paginated SLA data.
    """
    permission_classes = [CozentusPermission]

    @extend_schema(request=SLAFilterSerializer, responses=SLAReadSerializer)
    def post(self, request):
        try:
            order_by = request.data.pop('order_by', None)
            order_type = request.data.pop('order_type', None)
            page_size = request.data.get("page_size", 50)
            page = request.data.get("page", 1)

            if page < 1 or page_size < 1:
                logger.warning('Invalid page or page size provided')
                return Response({"message": "Page and page size should be positive integers"},
                                status=status.HTTP_400_BAD_REQUEST)

            serializer = SLAFilterSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            data = serializer.validated_data

            filter_dict = {
                "department": "department_id",
                "department_name": "department__department_name__icontains",
                "is_delete": "is_delete",
                "is_active": "is_active",
            }

            query_filter = {filter_dict[key]: value for key, value in data.items() if
                            key in filter_dict and value is not None}
            slas = SLA.objects.filter(**query_filter)

            order_by_dict = {
                "department_name": "department__department_name",
                "response_time": "response_time",
                "resolution_time": "resolution_time",
                "is_active": "is_active",
            }

            query_order_by = order_by_dict.get(order_by)
            if order_type == "desc" and query_order_by:
                query_order_by = f"-{query_order_by}"
            if query_order_by:
                slas = slas.order_by(query_order_by)

            paginator = Paginator(slas, page_size)
            number_pages = paginator.num_pages

            if page > number_pages and page > 1:
                logger.info('Page number out of range')
                return Response({"message": "Page not found"}, status=status.HTTP_400_BAD_REQUEST)

            page_obj = paginator.get_page(page)
            results = SLAReadSerializer(page_obj, many=True)

            logger.info('SLA data fetched successfully')
            return Response({'count': slas.count(), 'results': results.data}, status=status.HTTP_200_OK)

        except serializers.ValidationError as ve:
            logger.warning(f'Validation error: {ve.detail}', exc_info=True)
            return Response(ve.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ee:
            logger.warning(f'Unexpected error: {str(ee)}', exc_info=True)
            return Response(str(ee), status=status.HTTP_400_BAD_REQUEST)
