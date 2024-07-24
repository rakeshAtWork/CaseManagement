from django.core.paginator import Paginator
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.views import APIView
from acl.privilege import CozentusPermission
from acl.export_excel import export_query_to_excel
from master_data_management.models import FileType, Client, BusinessUnit, Vendor, Application, Customer
from master_data_management.permissions import permission_file_type_create, permission_file_type_view, \
    permission_file_type_edit, permission_file_type_delete, permission_file_type_list, permission_client_create, \
    permission_client_view, permission_client_edit, permission_client_delete, permission_client_list, \
    permission_customer_create, permission_customer_view, permission_customer_edit, permission_customer_delete, \
    permission_customer_list, permission_business_unit_create, permission_business_unit_view, \
    permission_business_unit_edit, permission_business_unit_delete, permission_business_unit_list, \
    permission_vendor_create, permission_vendor_view, permission_vendor_edit, permission_vendor_delete, \
    permission_vendor_list, permission_application_create, permission_application_view, permission_application_delete, \
    permission_application_edit, permission_application_list
from master_data_management.serializers import (FileTypeSerializers, FileTypeReadSerializers, FileTypeFilterSerializers,
                                                ClientSerializers, ClientReadSerializers, ClientFilterSerializers,
                                                BusinessUnitSerializers,
                                                BusinessUnitReadSerializers, BusinessUnitFilterSerializers,
                                                VendorSerializers, VendorReadSerializers,
                                                VendorFilterSerializers, ApplicationSerializers,
                                                ApplicationReadSerializers, ApplicationFilterSerializers,
                                                CustomerSerializers, CustomerReadSerializers, CustomerFilterSerializers)
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response


class FileTypeApi(CreateAPIView):
    """
    File Type Create api view
    """
    case_management_object_permissions = {
        'POST': (permission_file_type_create,)
    }
    permission_classes = [CozentusPermission]
    serializer_class = FileTypeSerializers
    queryset = FileType.objects.all()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user.id)


class FileTypeModifyApi(RetrieveUpdateDestroyAPIView):
    """
    File Type api view
    """
    case_management_object_permissions = {
        'GET': (permission_file_type_view,),
        'PUT': (permission_file_type_edit,),
        'PATCH': (permission_file_type_edit,),
        'DELETE': (permission_file_type_delete,)
    }
    permission_classes = (CozentusPermission,)
    serializer_class = FileTypeSerializers
    queryset = FileType.objects.all()

    def perform_update(self, serializer):
        serializer.save(modified_by=self.request.user.id,
                        modified_on=timezone.now().astimezone(timezone.timezone.utc))


class FileTypeFilterApi(APIView):
    """
    File Type filter api
    """
    case_management_object_permissions = {
        'POST': (permission_file_type_list,)
    }
    permission_classes = (CozentusPermission,)
    serializer_class = FileTypeReadSerializers

    @swagger_auto_schema(request_body=FileTypeFilterSerializers)
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
            serializer = FileTypeFilterSerializers(data=request.data)
            serializer.is_valid(raise_exception=True)
            data = serializer.data
            filter_dict = {
                "status": "status", "file_type": "file_type__icontains",
                "file_extension": "file_extension__icontains",
                "max_file_size": "max_file_size__icontains", "file_description": "file_description__icontains",
                "created_on": "created_on", "created_by": "created_by",
                "modified_on": "modified_on", "modified_by": "modified_by"
            }
            query_dict = {filter_dict.get(key, None): value for key, value in data.items() if
                          value or isinstance(value, (int, bool))}
            query_dict = {key: value for key, value in query_dict.items() if key}
            query_dict["is_delete"] = False
            queryset = FileType.objects.filter(**query_dict).order_by('-created_on')
            order_dict = {
                "status": "status", "file_type": "file_type",
                "file_extension": "file_extension",
                "max_file_size": "max_file_size", "file_description": "file_description",
                "created_on": "created_on", "created_by": "created_by",
                "modified_on": "modified_on", "modified_by": "modified_by"
            }
            query_filter = order_dict.get(order_by, None)
            if query_filter:
                if order_type == "desc":
                    query_filter = f"-{query_filter}"
                queryset = queryset.order_by(query_filter)
            if data.get("export"):
                results = self.serializer_class(queryset, many=True)
                return export_query_to_excel(data=results.data, module_name="FILE_TYPE")
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


class ClientApi(CreateAPIView):
    """
    Client Create api view
    """
    case_management_object_permissions = {
        'POST': (permission_client_create,)
    }
    permission_classes = [CozentusPermission]
    serializer_class = ClientSerializers
    queryset = Client.objects.all()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user.id)


class ClientModifyApi(RetrieveUpdateDestroyAPIView):
    """
    Client api view
    """
    case_management_object_permissions = {
        'GET': (permission_client_view,),
        'PUT': (permission_client_edit,),
        'PATCH': (permission_client_edit,),
        'DELETE': (permission_client_delete,)
    }
    permission_classes = (CozentusPermission,)
    serializer_class = ClientSerializers
    queryset = Client.objects.all()

    def perform_update(self, serializer):
        serializer.save(modified_by=self.request.user.id,
                        modified_on=timezone.now().astimezone(timezone.timezone.utc))


class ClientFilterApi(APIView):
    """
    Client filter api
    """
    case_management_object_permissions = {
        'POST': (permission_client_list,)
    }
    permission_classes = (CozentusPermission,)
    serializer_class = ClientReadSerializers

    @swagger_auto_schema(request_body=ClientFilterSerializers)
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
            serializer = ClientFilterSerializers(data=request.data)
            serializer.is_valid(raise_exception=True)
            data = serializer.data
            filter_dict = {
                "status": "status", "code": "code__icontains",
                "name": "name__icontains",
                "contact_name": "contact_name__icontains", "contact_email": "contact_email__icontains",
                "contact_number": "contact_number__icontains",
                "created_on": "created_on", "created_by": "created_by",
                "modified_on": "modified_on", "modified_by": "modified_by"
            }
            query_dict = {filter_dict.get(key, None): value for key, value in data.items() if
                          value or isinstance(value, (int, bool))}
            query_dict = {key: value for key, value in query_dict.items() if key}
            queryset = Client.objects.filter(**query_dict).order_by('-created_on')
            order_dict = {
                "status": "status", "code": "code",
                "name": "name",
                "contact_name": "contact_name", "contact_email": "contact_email",
                "contact_number": "contact_number",
                "created_on": "created_on", "created_by": "created_by",
                "modified_on": "modified_on", "modified_by": "modified_by"
            }
            query_filter = order_dict.get(order_by, None)
            if query_filter:
                if order_type == "desc":
                    query_filter = f"-{query_filter}"
                queryset = queryset.order_by(query_filter)
            if data.get("export"):
                results = self.serializer_class(queryset, many=True)
                return export_query_to_excel(data=results.data, module_name="CLIENT")
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


class CustomerApi(CreateAPIView):
    """
    Customer Create api view
    """
    case_management_object_permissions = {
        'POST': (permission_customer_create,)
    }
    permission_classes = [CozentusPermission]
    serializer_class = CustomerSerializers
    queryset = Customer.objects.all()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user.id)


class CustomerModifyApi(RetrieveUpdateDestroyAPIView):
    """
    Customer api view
    """
    case_management_object_permissions = {
        'GET': (permission_customer_view,),
        'PUT': (permission_customer_edit,),
        'PATCH': (permission_customer_edit,),
        'DELETE': (permission_customer_delete,)
    }
    permission_classes = [CozentusPermission]
    serializer_class = CustomerSerializers
    queryset = Customer.objects.all()

    def perform_update(self, serializer):
        serializer.save(modified_by=self.request.user.id,
                        modified_on=timezone.now().astimezone(timezone.timezone.utc))


class CustomerFilterApi(APIView):
    """
    Customer filter api
    """
    case_management_object_permissions = {
        'POST': (permission_customer_list,)
    }
    permission_classes = (CozentusPermission,)
    serializer_class = CustomerReadSerializers

    @swagger_auto_schema(request_body=CustomerFilterSerializers)
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
            serializer = CustomerFilterSerializers(data=request.data)
            serializer.is_valid(raise_exception=True)
            data = serializer.data
            filter_dict = {
                "status": "status", "code": "code__icontains",
                "name": "name__icontains", "disposal_action": "disposal_action__icontains",
                "contact_name": "contact_name__icontains", "contact_email": "contact_email__icontains",
                "contact_number": "contact_number__icontains",
                "created_on": "created_on", "created_by": "created_by",
                "modified_on": "modified_on", "modified_by": "modified_by",
                "disposal_notification_period": "disposal_notification_period",
                "retention_period": "retention_period"
            }
            query_dict = {filter_dict.get(key, None): value for key, value in data.items() if
                          value or isinstance(value, (int, bool))}
            query_dict = {key: value for key, value in query_dict.items() if key}
            queryset = Customer.objects.filter(**query_dict).order_by('-created_on')
            order_dict = {
                "status": "status", "code": "code",
                "name": "name", "disposal_notification_period": "disposal_notification_period",
                "contact_name": "contact_name", "contact_email": "contact_email",
                "contact_number": "contact_number", "disposal_action": "disposal_action",
                "created_on": "created_on", "created_by": "created_by",
                "modified_on": "modified_on", "modified_by": "modified_by", "retention_period": "retention_period"
            }
            query_filter = order_dict.get(order_by, None)
            if query_filter:
                if order_type == "desc":
                    query_filter = f"-{query_filter}"
                queryset = queryset.order_by(query_filter)
            if data.get("export"):
                results = self.serializer_class(queryset, many=True)
                return export_query_to_excel(data=results.data, module_name="CUSTOMER")
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


class BusinessUnitApi(CreateAPIView):
    """
    BusinessUnit Create api view
    """
    case_management_object_permissions = {
        'POST': (permission_business_unit_create,)
    }
    permission_classes = [CozentusPermission]
    serializer_class = BusinessUnitSerializers
    queryset = BusinessUnit.objects.all()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user.id)


class BusinessUnitModifyApi(RetrieveUpdateDestroyAPIView):
    """
    BusinessUnit api view
    """
    case_management_object_permissions = {
        'GET': (permission_business_unit_view,),
        'PUT': (permission_business_unit_edit,),
        'PATCH': (permission_business_unit_edit,),
        'DELETE': (permission_business_unit_delete,)
    }
    permission_classes = (CozentusPermission,)
    serializer_class = BusinessUnitSerializers
    queryset = BusinessUnit.objects.all()

    def perform_update(self, serializer):
        serializer.save(modified_by=self.request.user.id,
                        modified_on=timezone.now().astimezone(timezone.timezone.utc))


class BusinessUnitFilterApi(APIView):
    """
    BusinessUnit filter api
    """
    case_management_object_permissions = {
        'POST': (permission_business_unit_list,)
    }
    permission_classes = (CozentusPermission,)
    serializer_class = BusinessUnitReadSerializers

    @swagger_auto_schema(request_body=BusinessUnitFilterSerializers)
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
            serializer = BusinessUnitFilterSerializers(data=request.data)
            serializer.is_valid(raise_exception=True)
            data = serializer.data
            filter_dict = {
                "client_id": "client_id", "code": "code__icontains",
                "name": "name__icontains", "status": "status",
                "contact_name": "contact_name__icontains", "contact_email": "contact_email__icontains",
                "contact_number": "contact_number__icontains",
                "created_on": "created_on", "created_by": "created_by", "is_delete": "is_delete",
                "modified_on": "modified_on", "modified_by": "modified_by"
            }
            query_dict = {filter_dict.get(key, None): value for key, value in data.items() if
                          value or isinstance(value, (int, bool))}
            query_dict = {key: value for key, value in query_dict.items() if key}
            query_dict["is_delete"] = False
            queryset = BusinessUnit.objects.filter(**query_dict).order_by('-created_on')
            order_dict = {
                "client_id": "client_id", "code": "code",
                "name": "name", "status": "status",
                "contact_name": "contact_name", "contact_email": "contact_email",
                "contact_number": "contact_number", "is_delete": "is_delete",
                "created_on": "created_on", "created_by": "created_by",
                "modified_on": "modified_on", "modified_by": "modified_by"
            }
            query_filter = order_dict.get(order_by, None)
            if query_filter:
                if order_type == "desc":
                    query_filter = f"-{query_filter}"
                queryset = queryset.order_by(query_filter)
            if data.get("export"):
                results = self.serializer_class(queryset, many=True)
                return export_query_to_excel(data=results.data, module_name="BUSINESS_UNIT")
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


class VendorApi(CreateAPIView):
    """
    Vendor Create api view
    """
    case_management_object_permissions = {
        'POST': (permission_vendor_create,)
    }
    permission_classes = [CozentusPermission]
    serializer_class = VendorSerializers
    queryset = Vendor.objects.all()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user.id)


class VendorModifyApi(RetrieveUpdateDestroyAPIView):
    """
    Vendor api view
    """
    case_management_object_permissions = {
        'GET': (permission_vendor_view,),
        'PUT': (permission_vendor_edit,),
        'PATCH': (permission_vendor_edit,),
        'DELETE': (permission_vendor_delete,)
    }
    permission_classes = (CozentusPermission,)
    serializer_class = VendorSerializers
    queryset = Vendor.objects.all()

    def perform_update(self, serializer):
        serializer.save(modified_by=self.request.user.id,
                        modified_on=timezone.now().astimezone(timezone.timezone.utc))


class VendorFilterApi(APIView):
    """
    Vendor filter api
    """
    case_management_object_permissions = {
        'POST': (permission_vendor_list,)
    }
    permission_classes = (CozentusPermission,)
    serializer_class = VendorReadSerializers

    @swagger_auto_schema(request_body=VendorFilterSerializers)
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
            serializer = VendorFilterSerializers(data=request.data)
            serializer.is_valid(raise_exception=True)
            data = serializer.data
            filter_dict = {
                "status": "status", "customer_id": "client_id", "code": "code__icontains",
                "name": "name__icontains", "disposal_action": "disposal_action__icontains",
                "contact_name": "contact_name__icontains", "contact_email": "contact_email__icontains",
                "contact_number": "contact_number__icontains", "is_delete": "is_delete",
                "created_on": "created_on", "created_by": "created_by",
                "modified_on": "modified_on", "modified_by": "modified_by", "retention_period": "retention_period",
                "disposal_notification_period": "disposal_notification_period"
            }
            query_dict = {filter_dict.get(key, None): value for key, value in data.items() if
                          value or isinstance(value, (int, bool))}
            query_dict = {key: value for key, value in query_dict.items() if key}
            queryset = Vendor.objects.filter(**query_dict).order_by('-created_on')
            order_dict = {
                "status": "status", "customer_id": "client_id", "code": "code",
                "name": "name", "disposal_action": "disposal_action",
                "contact_name": "contact_name", "contact_email": "contact_email",
                "contact_number": "contact_number", "is_delete": "is_delete",
                "created_on": "created_on", "created_by": "created_by",
                "modified_on": "modified_on", "modified_by": "modified_by", "retention_period": "retention_period",
                "disposal_notification_period": "disposal_notification_period"
            }
            query_filter = order_dict.get(order_by, None)
            if query_filter:
                if order_type == "desc":
                    query_filter = f"-{query_filter}"
                queryset = queryset.order_by(query_filter)
            if data.get("export"):
                results = self.serializer_class(queryset, many=True)
                return export_query_to_excel(data=results.data, module_name="VENDOR")
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


class ApplicationApi(CreateAPIView):
    """
    Application Create api view
    """
    case_management_object_permissions = {
        'POST': (permission_application_create,)
    }
    permission_classes = [CozentusPermission]
    serializer_class = ApplicationSerializers
    queryset = Application.objects.all()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user.id)


class ApplicationModifyApi(RetrieveUpdateDestroyAPIView):
    """
    Application api view
    """
    case_management_object_permissions = {
        'GET': (permission_application_view,),
        'PUT': (permission_application_edit,),
        'PATCH': (permission_application_edit,),
        'DELETE': (permission_application_delete,)
    }
    permission_classes = (CozentusPermission,)
    serializer_class = ApplicationSerializers
    queryset = Application.objects.all()

    def perform_update(self, serializer):
        serializer.save(modified_by=self.request.user.id,
                        modified_on=timezone.now().astimezone(timezone.timezone.utc))


class ApplicationFilterApi(APIView):
    """
    Application filter api
    """
    case_management_object_permissions = {
        'POST': (permission_application_list,)
    }
    permission_classes = (CozentusPermission,)
    serializer_class = ApplicationReadSerializers

    @swagger_auto_schema(request_body=ApplicationFilterSerializers)
    def post(self, request):
        """
        This method is used for retrieving role permission data with pagination and filter
        """
        try:
            order_by = request.data.get('order_by')
            order_type = request.data.get('order_type')
            serializer = ApplicationFilterSerializers(data=request.data)
            serializer.is_valid(raise_exception=True)
            data = serializer.data
            filter_dict = {
                "code": "code__icontains", "contact_name": "contact_name__icontains",
                "contact_email": "contact_email__icontains", "status": "status",
                "name": "name__icontains", "contact_number": "contact_number__icontains",
                "created_on": "created_on", "created_by": "created_by",
                "modified_on": "modified_on", "modified_by": "modified_by"
            }
            query_dict = {filter_dict.get(key, None): value for key, value in data.items() if
                          value or isinstance(value, (int, bool))}
            query_dict = {key: value for key, value in query_dict.items() if key}
            queryset = Application.objects.filter(**query_dict).order_by('-created_on')
            order_dict = {
                "code": "code__icontains", "contact_name": "contact_name", "contact_email": "contact_email",
                "name": "name__icontains", "contact_number": "contact_number",
                "created_on": "created_on", "created_by": "created_by", "status": "status",
                "modified_on": "modified_on", "modified_by": "modified_by"
            }
            query_filter = order_dict.get(order_by, None)
            if query_filter:
                if order_type == "desc":
                    query_filter = f"-{query_filter}"
                queryset = queryset.order_by(query_filter)
            serializer = self.serializer_class(queryset, many=True)
            serializer_data = serializer.data
            # if data.get("export"):
            #     return export_query_to_excel(serializer_data, module_name="RULES_SETUP")
            return Response({"count": queryset.count(), "results": serializer_data})

        except ValueError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ee:
            return Response(str(ee), status=status.HTTP_400_BAD_REQUEST)
