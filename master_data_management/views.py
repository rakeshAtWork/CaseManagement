from django.core.exceptions import FieldError
from django.core.paginator import Paginator
from drf_spectacular.utils import extend_schema
from rest_framework import generics, serializers
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import RetrieveUpdateDestroyAPIView, CreateAPIView, ListCreateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from acl.privilege import CozentusPermission
from acl.export_excel import export_query_to_excel
from master_data_management.models import FileType, Client, BusinessUnit, Vendor, Application, Customer, AccountType, \
    SupplierContactDetails, D365FOSetup, CompanyInfoForValidation, CPPSanctionAssessment, VendorDetails, Currency, \
    Country, Category, Department, UserDepartment, Status, EmailTemplate
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
                                                CustomerSerializers, CustomerReadSerializers, CustomerFilterSerializers,
                                                AccountTypeSerializer, SupplierContactDetailsSerializer,
                                                D365FOSetupSerializer, CompanyInfoForValidationSerializer,
                                                CPPSanctionAssessmentSerializer, VendorDetailsSerializer,
                                                UpdateVendorDetailsSerializer, VendorDetailsFilterSerializer,
                                                D365FOSetupReadSerializer, D365FOSetupFilterSerializer,
                                                SupplierContactDetailsReadSerializer,
                                                SupplierContactDetailsFilterSerializer, CurrencySerializer,
                                                CountrySerializer, CountryFilterSerializer, CountryReadSerializer,
                                                CurrencyFilterSerializer, CurrencyReadSerializer,
                                                CategoryFilterSerializer, CategorySerializer, DepartmentReadSerializer,
                                                DepartmentFilterSerializer, DepartmentSerializer,
                                                UserDepartmentSerializer, StatusSerializer, StatusFilterSerializer,
                                                EmailTemplateSerializer, EmailTemplateFilterSerializer,
                                                EmailTemplateReadSerializer)
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
        serializer.save(updated_by=self.request.user.id,
                        updated_on=timezone.now().astimezone(timezone.timezone.utc))


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
                "updated_on": "updated_on", "updated_by": "updated_by"
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
                "updated_on": "updated_on", "updated_by": "updated_by"
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
        serializer.save(updated_by=self.request.user.id,
                        updated_on=timezone.now().astimezone(timezone.timezone.utc))


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
                "updated_on": "updated_on", "updated_by": "updated_by"
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
                "updated_on": "updated_on", "updated_by": "updated_by"
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
        serializer.save(updated_by=self.request.user.id,
                        updated_on=timezone.now().astimezone(timezone.timezone.utc))


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
                "updated_on": "updated_on", "updated_by": "updated_by",
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
                "updated_on": "updated_on", "updated_by": "updated_by", "retention_period": "retention_period"
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
        serializer.save(updated_by=self.request.user.id,
                        updated_on=timezone.now().astimezone(timezone.timezone.utc))


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
                "updated_on": "updated_on", "updated_by": "updated_by"
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
                "updated_on": "updated_on", "updated_by": "updated_by"
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
        serializer.save(updated_by=self.request.user.id,
                        updated_on=timezone.now().astimezone(timezone.timezone.utc))


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
                "updated_on": "updated_on", "updated_by": "updated_by", "retention_period": "retention_period",
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
                "updated_on": "updated_on", "updated_by": "updated_by", "retention_period": "retention_period",
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
        serializer.save(updated_by=self.request.user.id,
                        updated_on=timezone.now().astimezone(timezone.timezone.utc))


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
                "updated_on": "updated_on", "updated_by": "updated_by"
            }
            query_dict = {filter_dict.get(key, None): value for key, value in data.items() if
                          value or isinstance(value, (int, bool))}
            query_dict = {key: value for key, value in query_dict.items() if key}
            queryset = Application.objects.filter(**query_dict).order_by('-created_on')
            order_dict = {
                "code": "code__icontains", "contact_name": "contact_name", "contact_email": "contact_email",
                "name": "name__icontains", "contact_number": "contact_number",
                "created_on": "created_on", "created_by": "created_by", "status": "status",
                "updated_on": "updated_on", "updated_by": "updated_by"
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


class VendorDetailsCreateView(CreateAPIView):
    queryset = VendorDetails.objects.all()
    serializer_class = VendorDetailsSerializer


class VendorDetailsRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = VendorDetails.objects.all()
    serializer_class = UpdateVendorDetailsSerializer


class VendorDetailsFilterApi(APIView):
    """
    VendorDetails filter api
    """
    permission_classes = [IsAuthenticated]
    serializer_class = VendorDetailsFilterSerializer

    @swagger_auto_schema(request_body=VendorDetailsFilterSerializer)
    def post(self, request):
        """
        Retrieve VendorDetails data with pagination and filter
        """
        try:
            order_by = request.data.get('order_by', 'created_on')
            order_type = request.data.get('order_type', 'asc')
            serializer = VendorDetailsFilterSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            data = serializer.validated_data
            filter_dict = {
                "company_code": "company_code__icontains",
                "company_name": "company_name__icontains",
                "agent_number": "agent_number__icontains",
                "supplier_type": "supplier_type__icontains",
                "currency": "currency__icontains",
                "terms_of_payment": "terms_of_payment__icontains",
                "supplier_name": "supplier_name__icontains",
                "siret_number": "siret_number__icontains",
                "vat_country_code": "vat_country_code__icontains",
                "orbis_id": "orbis_id__icontains",
                "orbis_id_found": "orbis_id_found",
                "address_line": "address_line__icontains",
                "country": "country__icontains",
                "postal_code": "postal_code__icontains",
                "town": "town__icontains",
                "country_code": "country_code__icontains",
                "swift_number": "swift_number__icontains",
                "is_prime_revenue": "is_prime_revenue",
                "created_by": "created_by",
                "updated_by": "updated_by",
                "created_on": "created_on",
                "updated_on": "updated_on"
            }
            query_dict = {filter_dict.get(key, None): value for key, value in data.items() if
                          value or isinstance(value, (int, bool))}
            queryset = VendorDetails.objects.filter(**query_dict).order_by('-created_on')
            if order_type == "desc":
                order_by = f"-{order_by}"
            queryset = queryset.order_by(order_by)
            serializer = VendorDetailsSerializer(queryset, many=True)
            return Response({"count": queryset.count(), "results": serializer.data})
        except ValueError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# AccountType Views
class AccountTypeListApi(generics.ListAPIView):
    queryset = AccountType.objects.filter(is_delete=False)
    serializer_class = AccountTypeSerializer
    permission_classes = [IsAuthenticated]


class AccountTypeModifyApi(RetrieveUpdateDestroyAPIView):
    queryset = AccountType.objects.filter(is_delete=False)
    serializer_class = AccountTypeSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'  # Use the primary key

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user.id)

    def perform_destroy(self, instance):
        instance.is_delete = True
        instance.save()


# SupplierContactDetails Views
class SupplierContactDetailsListApi(generics.ListAPIView):
    queryset = SupplierContactDetails.objects.filter(is_delete=False)
    serializer_class = SupplierContactDetailsSerializer
    permission_classes = [CozentusPermission]


class SupplierContactDetailsModifyApi(RetrieveUpdateDestroyAPIView):
    queryset = SupplierContactDetails.objects.filter(is_delete=False)
    serializer_class = SupplierContactDetailsSerializer
    permission_classes = [CozentusPermission]

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user.id)

    def perform_destroy(self, instance):
        instance.is_delete = True
        instance.save()


# D365FOSetup Views
class D365FOSetupListApi(generics.ListAPIView):
    queryset = D365FOSetup.objects.filter(is_delete=False)
    serializer_class = D365FOSetupSerializer
    permission_classes = [CozentusPermission]


class D365FOSetupModifyApi(RetrieveUpdateDestroyAPIView):
    queryset = D365FOSetup.objects.filter(is_delete=False)
    serializer_class = D365FOSetupSerializer
    permission_classes = [CozentusPermission]

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user.id)

    def perform_destroy(self, instance):
        instance.is_delete = True
        instance.save()


# CompanyInfoForValidation Views
class CompanyInfoForValidationListApi(generics.ListAPIView):
    queryset = CompanyInfoForValidation.objects.filter(is_delete=False)
    serializer_class = CompanyInfoForValidationSerializer
    permission_classes = [IsAuthenticated]


class CompanyInfoForValidationModifyApi(RetrieveUpdateDestroyAPIView):
    queryset = CompanyInfoForValidation.objects.filter(is_delete=False)
    serializer_class = CompanyInfoForValidationSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'  # Use the primary key

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user.id)

    def perform_destroy(self, instance):
        instance.is_delete = True
        instance.save()


# CPPSanctionAssessment Views
class CPPSanctionAssessmentListApi(generics.ListAPIView):
    queryset = CPPSanctionAssessment.objects.filter(is_delete=False)
    serializer_class = CPPSanctionAssessmentSerializer
    permission_classes = [IsAuthenticated]


class CPPSanctionAssessmentModifyApi(RetrieveUpdateDestroyAPIView):
    queryset = CPPSanctionAssessment.objects.filter(is_delete=False)
    serializer_class = CPPSanctionAssessmentSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'  # Use the primary key

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user.id)

    def perform_destroy(self, instance):
        instance.is_delete = True
        instance.save()


class D365FOSetupFilterApi(APIView):
    permission_classes = (CozentusPermission,)
    case_management_object_permissions = {
        # 'POST': (permission_d365fo_setup_create,),  # Replace with actual permissions
    }

    @extend_schema(request=D365FOSetupFilterSerializer, responses=D365FOSetupReadSerializer)
    def post(self, request):
        """
        This method is used to make a POST request for pagination, filtering, and returning D365FOSetup data.
        """
        try:
            order_by = request.data.pop('order_by', None)
            order_type = request.data.pop('order_type', None)
            page_size = request.data.get("page_size", 50)
            page = request.data.get("page", 1)

            if page < 1 or page_size < 1:
                return Response({"message": "Page and page size should be positive integers"},
                                status=status.HTTP_400_BAD_REQUEST)

            serializer = D365FOSetupFilterSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            data = serializer.validated_data

            filter_dict = {
                "sales_tax_group": "sales_tax_group__icontains",
                "vendor_group": "vendor_group__icontains",
                "payment_method": "payment_method__icontains",
                "business_unit": "business_unit__icontains",
                "inter_company": "inter_company",
                "vendor_hold": "vendor_hold",
                "source_system": "source_system__icontains",
                "source_system_supplier_reference": "source_system_supplier_reference__icontains",
                "d365fo_id": "d365fo_id__icontains",
                "fs_ticket_number": "fs_ticket_number__icontains",
                "allow_false_duplicates": "allow_false_duplicates",
            }

            query_filter = {filter_dict[key]: value for key, value in data.items() if
                            key in filter_dict and value is not None}
            d365fo_setups = D365FOSetup.objects.filter(**query_filter)

            order_by_dict = {
                "sales_tax_group": "sales_tax_group",
                "vendor_group": "vendor_group",
                "payment_method": "payment_method",
                "business_unit": "business_unit",
                "source_system": "source_system",
                "d365fo_id": "d365fo_id",
                "fs_ticket_number": "fs_ticket_number",
                "created_on": "created_on",
                "updated_on": "updated_on",
            }

            query_order_by = order_by_dict.get(order_by)

            if order_type == "desc" and query_order_by:
                query_order_by = f"-{query_order_by}"

            if query_order_by:
                d365fo_setups = d365fo_setups.order_by(query_order_by)

            paginator = Paginator(d365fo_setups, page_size)
            number_pages = paginator.num_pages

            if page > number_pages and page > 1:
                return Response({"message": "Page not found"}, status=status.HTTP_400_BAD_REQUEST)

            page_obj = paginator.get_page(page)
            results = D365FOSetupReadSerializer(page_obj, many=True)

            return Response({'count': d365fo_setups.count(), 'results': results.data}, status=status.HTTP_200_OK)

        except FieldError as fe:
            return Response({"message": str(fe)}, status=status.HTTP_400_BAD_REQUEST)

        except serializers.ValidationError as ve:
            return Response({"message": str(ve)}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as ee:
            return Response({"message": str(ee)}, status=status.HTTP_400_BAD_REQUEST)


class SupplierContactDetailsFilterApi(APIView):
    permission_classes = (CozentusPermission,)
    case_management_object_permissions = {
        # 'POST': (permission_supplier_contact_details_create,),  # Replace with actual permissions
    }

    @extend_schema(request=SupplierContactDetailsFilterSerializer, responses=SupplierContactDetailsReadSerializer)
    def post(self, request):
        """
        This method is used to make a POST request for pagination, filtering, and returning SupplierContactDetails data.
        """
        try:
            order_by = request.data.pop('order_by', None)
            order_type = request.data.pop('order_type', None)
            page_size = request.data.get("page_size", 50)
            page = request.data.get("page", 1)

            if page < 1 or page_size < 1:
                return Response({"message": "Page and page size should be positive integers"},
                                status=status.HTTP_400_BAD_REQUEST)

            serializer = SupplierContactDetailsFilterSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            data = serializer.validated_data

            filter_dict = {
                "contact_person": "contact_person__icontains",
                "main_phone_number": "main_phone_number__icontains",
                "main_email_id": "main_email_id__icontains",
                "finance_phone_number": "finance_phone_number__icontains",
                "finance_email_id": "finance_email_id__icontains",
                "remittance_email_id": "remittance_email_id__icontains",
                "email_for_receiving_po": "email_for_receiving_po__icontains",
                "email_id_for_quote": "email_id_for_quote__icontains",
                "is_delete": "is_delete",
            }

            query_filter = {filter_dict[key]: value for key, value in data.items() if
                            key in filter_dict and value is not None}
            supplier_contacts = SupplierContactDetails.objects.filter(**query_filter)

            order_by_dict = {
                "contact_person": "contact_person",
                "main_phone_number": "main_phone_number",
                "main_email_id": "main_email_id",
                "created_on": "created_on",
                "updated_on": "updated_on",
            }

            query_order_by = order_by_dict.get(order_by)

            if order_type == "desc" and query_order_by:
                query_order_by = f"-{query_order_by}"

            if query_order_by:
                supplier_contacts = supplier_contacts.order_by(query_order_by)

            paginator = Paginator(supplier_contacts, page_size)
            number_pages = paginator.num_pages

            if page > number_pages and page > 1:
                return Response({"message": "Page not found"}, status=status.HTTP_400_BAD_REQUEST)

            page_obj = paginator.get_page(page)
            results = SupplierContactDetailsReadSerializer(page_obj, many=True)

            return Response({'count': supplier_contacts.count(), 'results': results.data}, status=status.HTTP_200_OK)

        except FieldError as fe:
            return Response({"message": str(fe)}, status=status.HTTP_400_BAD_REQUEST)

        except serializers.ValidationError as ve:
            return Response({"message": str(ve)}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as ee:
            return Response({"message": str(ee)}, status=status.HTTP_400_BAD_REQUEST)


class CountryListCreateAPIView(generics.ListCreateAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = [CozentusPermission]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user.id, updated_by=self.request.user.id)


class CountryRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = [CozentusPermission]

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user.id)

    def perform_destroy(self, instance):
        instance.is_delete = True
        instance.save()


class CurrencyListCreateAPIView(generics.ListCreateAPIView):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
    permission_classes = [CozentusPermission]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user.id, updated_by=self.request.user.id)


class CurrencyRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
    permission_classes = [CozentusPermission]

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user.id)

    def perform_destroy(self, instance):
        instance.is_delete = True
        instance.save()


class CountryCreateApi(CreateAPIView):
    """
        Country Create api view
    """
    case_management_object_permissions = {
        # 'POST': (permission_country_create,)
    }
    permission_classes = [CozentusPermission]
    serializer_class = CountrySerializer
    queryset = Country.objects.all()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user.id)


class CountryModifyApi(RetrieveUpdateDestroyAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user.id)

    def perform_destroy(self, instance):
        instance.is_delete = True
        instance.save()


class CountryFilterApi(APIView):
    """
    Country filter API to retrieve filtered and paginated country data.
    """
    permission_classes = [CozentusPermission]

    @extend_schema(request=CountryFilterSerializer, responses=CountryReadSerializer)
    def post(self, request):
        try:
            order_by = request.data.pop('order_by', None)
            order_type = request.data.pop('order_type', None)
            page_size = request.data.get("page_size", 50)
            page = request.data.get("page", 1)

            if page < 1 or page_size < 1:
                return Response({"message": "page and page size should be positive integers"},
                                status=status.HTTP_400_BAD_REQUEST)

            serializer = CountryFilterSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            data = serializer.validated_data

            filter_dict = {
                "country_name": "country_name__icontains",
                "country_code": "country_code__icontains",
                "description": "description__icontains",
                "created_by": "created_by",
                "is_active": "is_active"
            }

            query_filter = {filter_dict[key]: value for key, value in data.items() if
                            key in filter_dict and value is not None}
            countries = Country.objects.filter(**query_filter)

            order_by_dict = {
                "country_name": "country_name",
                "country_code": "country_code",
                "created_on": "created_on",
                "updated_on": "updated_on"
            }

            query_order_by = order_by_dict.get(order_by)
            if order_type == "desc" and query_order_by:
                query_order_by = f"-{query_order_by}"
            if query_order_by:
                countries = countries.order_by(query_order_by)

            paginator = Paginator(countries, page_size)
            number_pages = paginator.num_pages

            if page > number_pages and page > 1:
                return Response({"message": "Page not found"}, status=status.HTTP_400_BAD_REQUEST)

            page_obj = paginator.get_page(page)
            results = CountryReadSerializer(page_obj, many=True)

            return Response({'count': countries.count(), 'results': results.data}, status=status.HTTP_200_OK)

        except serializers.ValidationError as ve:
            raise serializers.ValidationError(ve.detail)
        except Exception as ee:
            return Response(str(ee), status=status.HTTP_400_BAD_REQUEST)


class CurrencyCreateApi(CreateAPIView):
    """
    Currency Create api view
    """
    case_management_object_permissions = {
        # 'POST': (permission_currency_create,)
    }
    permission_classes = [CozentusPermission]
    serializer_class = CurrencySerializer
    queryset = Currency.objects.all()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user.id)


class CurrencyModifyApi(RetrieveUpdateDestroyAPIView):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user.id)


class CurrencyFilterApi(APIView):
    """
    Currency filter API to retrieve filtered and paginated currency data.
    """
    permission_classes = [CozentusPermission]

    @extend_schema(request=CurrencyFilterSerializer, responses=CurrencyReadSerializer)
    def post(self, request):
        try:
            order_by = request.data.pop('order_by', None)
            order_type = request.data.pop('order_type', None)
            page_size = request.data.get("page_size", 50)
            page = request.data.get("page", 1)

            if page < 1 or page_size < 1:
                return Response({"message": "page and page size should be positive integers"},
                                status=status.HTTP_400_BAD_REQUEST)

            serializer = CurrencyFilterSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            data = serializer.validated_data

            filter_dict = {
                "currency_name": "currency_name__icontains",
                "currency_code": "currency_code__icontains",
                # "country_code": "country_code__icontains",
                "created_by": "created_by",
                "is_active": "is_active"
            }

            query_filter = {filter_dict[key]: value for key, value in data.items() if
                            key in filter_dict and value is not None}
            currencies = Currency.objects.filter(**query_filter)

            order_by_dict = {
                "currency_name": "currency_name",
                "currency_code": "currency_code",
                "created_on": "created_on",
                "updated_on": "updated_on"
            }

            query_order_by = order_by_dict.get(order_by)
            if order_type == "desc" and query_order_by:
                query_order_by = f"-{query_order_by}"
            if query_order_by:
                currencies = currencies.order_by(query_order_by)

            paginator = Paginator(currencies, page_size)
            number_pages = paginator.num_pages

            if page > number_pages and page > 1:
                return Response({"message": "Page not found"}, status=status.HTTP_400_BAD_REQUEST)

            page_obj = paginator.get_page(page)
            results = CurrencyReadSerializer(page_obj, many=True)

            return Response({'count': currencies.count(), 'results': results.data}, status=status.HTTP_200_OK)

        except serializers.ValidationError as ve:
            raise serializers.ValidationError(ve.detail)
        except Exception as ee:
            return Response(str(ee), status=status.HTTP_400_BAD_REQUEST)


class CategoryFilterApi(APIView):
    """
    This view class is used to return category data with filter and pagination
    """
    permission_classes = (CozentusPermission,)
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
    permission_classes = (CozentusPermission,)
    # cozentus_object_permissions = {
    #     'GET': (permission_department_list,),
    #     'POST': (permission_department_create,)
    # }
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


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
    permission_classes = (CozentusPermission,)
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user, updated_on=timezone.now())

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance:
            instance.delete()
            return Response({"message": "Category deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"message": "Record not found."}, status=status.HTTP_404_NOT_FOUND)


class DepartmentFilterApi(APIView):
    """
    This view class is used to return department data with filter and pagination
    """
    permission_classes = (CozentusPermission,)
    serializer_class = DepartmentReadSerializer
    cozentus_object_permissions = {
        # 'GET': (permission_department_view,),
        # 'PUT': (permission_department_update,),
        # 'PATCH': (permission_department_update,),
        # 'DELETE': (permission_department_delete,)

    }

    # permission_classes = (CozentusPermission,)

    # @swagger_auto_schema(request_body=DepartmentFilterSerializer)
    @extend_schema(request=DepartmentFilterSerializer, responses=DepartmentReadSerializer)
    def post(self, request):

        """
        This method is used to make post request for pagination and filter and return the department data.
        """
        try:
            order_by = request.data.pop('order_by', None)
            order_type = request.data.pop('order_type', None)
            page_size = request.data.get("page_size", 50)
            page = request.data.get("page", 1)
            is_active = request.data.get("is_active", None)

            if page < 1 or page_size < 1:
                return Response({"message": "page and page size should be positive integer"},
                                status=status.HTTP_400_BAD_REQUEST)

            serializer = DepartmentFilterSerializer(data=request.data)

            serializer.is_valid(raise_exception=True)
            data = serializer.validated_data

            filter_dict = {
                "department_name": "department_name__icontains",
                "department_code": "department_code__icontains",
                "department_type": "department_type",
                "is_active": "is_active",  # Adding is_active filter
            }

            query_filter = {filter_dict[key]: value for key, value in data.items() if
                            key in filter_dict and value is not None}

            # Apply the is_active filter
            if is_active:
                query_filter["is_active"] = is_active

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

            paginator = Paginator(departments, page_size)
            number_pages = paginator.num_pages

            if page > number_pages and page > 1:
                return Response({"message": "Page not found"}, status=status.HTTP_400_BAD_REQUEST)

            page_obj = paginator.get_page(page)
            results = DepartmentReadSerializer(page_obj, many=True)

            return Response({'count': departments.count(), 'results': results.data}, status=status.HTTP_200_OK)

        except FieldError as fe:
            print("Error 1")
            return Response({"message": str(fe)}, status=status.HTTP_400_BAD_REQUEST)

        except serializers.ValidationError as ve:
            print("Error 2")
            raise serializers.ValidationError(ve.detail)

        except Exception as ee:
            print("Error 3")
            return Response(str(ee), status=status.HTTP_400_BAD_REQUEST)


class DepartmentCreateApi(CreateAPIView):
    """
    This view class is used to Create a new department
    """
    permission_classes = (CozentusPermission,)
    serializer_class = DepartmentSerializer
    queryset = Department.objects.all()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class DepartmentUpdateApi(RetrieveUpdateDestroyAPIView):
    """
    This view class is used to update an existing department
    """
    permission_classes = (CozentusPermission,)
    serializer_class = DepartmentSerializer
    queryset = Department.objects.all()

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user, updated_on=timezone.now())

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance:
            instance.delete()
            return Response({"message": "Department deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"message": "Record not found."}, status=status.HTTP_404_NOT_FOUND)


class UserDepartmentApi(ListCreateAPIView):
    cozentus_object_permissions = {
        # 'GET': (permission_user_department_view,),
        # 'POST': (permission_user_department_create,)
    }
    permission_classes = (CozentusPermission,)
    serializer_class = UserDepartmentSerializer
    pagination_class = PageNumberPagination
    queryset = UserDepartment.objects.filter(is_delete=False)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def get_queryset(self):
        department_id = self.request.query_params.get('department_id', None)
        user_id = self.request.query_params.get('user_id', None)
        queryset = UserDepartment.objects.filter(is_delete=False)
        if department_id:
            queryset = queryset.filter(department=department_id)
        if user_id:
            queryset = queryset.filter(user=user_id)
        return queryset


class StatusCreateApi(CreateAPIView):
    """
    This view class is used to Create a new Status
    """
    permission_classes = (CozentusPermission,)
    serializer_class = StatusSerializer
    queryset = Status.objects.all()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class StatusUpdateApi(RetrieveUpdateDestroyAPIView):
    """
    This view class is used to update an existing status
    """
    permission_classes = (CozentusPermission,)
    serializer_class = StatusSerializer
    queryset = Status.objects.all()

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user, updated_at=timezone.now())

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
    permission_classes = (CozentusPermission,)
    serializer_class = StatusSerializer

    # @swagger_auto_schema(request_body=StatusReadSerializer)
    @extend_schema(request=StatusFilterSerializer, responses=StatusFilterSerializer)
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
            is_active = request.data.get('is_active', None)
            order_by = request.data.get('order_by')
            order_type = request.data.get('order_type')

            # Perform filtering based on the provided parameters
            queryset = Status.objects.all()
            if status_name:
                queryset = queryset.filter(status_name__icontains=status_name)
            if status_code:
                queryset = queryset.filter(status_code=status_code)
            if is_active is not None:
                queryset = queryset.filter(is_active=is_active)

            if order_by in ["status_name", "status_code"]:
                if order_type == "desc":
                    order_by = f"-{order_by}"
                queryset = queryset.order_by(order_by)

            paginator = Paginator(queryset, page_size)
            number_pages = paginator.num_pages
            if page > number_pages:
                return Response({"message": "Page not found"}, status=status.HTTP_400_BAD_REQUEST)

            # Get the page object for the requested page number
            page_obj = paginator.get_page(page)
            serializer = StatusFilterSerializer(page_obj, many=True)
            return Response({"count": len(queryset), "results": serializer.data})

        except Exception as ee:
            return Response({"message": "Please provide valid data"}, status=status.HTTP_400_BAD_REQUEST)


class EmailTemplateListCreateApi(generics.ListCreateAPIView):
    queryset = EmailTemplate.objects.all()
    serializer_class = EmailTemplateSerializer
    permission_classes = [CozentusPermission]

    def perform_create(self, serializer):
        serializer.save(
            created_by=self.request.user,
            created_on=timezone.now(),
        )


class EmailTemplateRetrieveUpdateDestroyApi(generics.RetrieveUpdateDestroyAPIView):
    queryset = EmailTemplate.objects.all()
    serializer_class = EmailTemplateSerializer
    permission_classes = [CozentusPermission]

    def perform_update(self, serializer):
        serializer.save(
            updated_by=self.request.user,
            updated_on=timezone.now(),
        )



class EmailTemplateFilterApi(APIView):
    """
    This view class is used to return email template data with filter and pagination.
    """
    permission_classes = (CozentusPermission,)
    serializer_class = EmailTemplateReadSerializer
    cozentus_object_permissions = {
        # 'GET': (permission_email_template_view,),
        # 'PUT': (permission_email_template_update,),
        # 'PATCH': (permission_email_template_update,),
        # 'DELETE': (permission_email_template_delete,)
    }

    @extend_schema(request=EmailTemplateFilterSerializer, responses=EmailTemplateReadSerializer)
    def post(self, request):
        """
        This method is used to make post request for pagination and filter and return the email template data.
        """
        try:
            order_by = request.data.pop('order_by', None)
            order_type = request.data.pop('order_type', None)
            page_size = request.data.get("page_size", 50)
            page = request.data.get("page", 1)
            is_active = request.data.get("is_active", None)

            if page < 1 or page_size < 1:
                return Response({"message": "page and page size should be positive integer"},
                                status=status.HTTP_400_BAD_REQUEST)

            serializer = EmailTemplateFilterSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            data = serializer.validated_data

            filter_dict = {
                "template_type": "template_type__icontains",
                "subject": "subject__icontains",
                "is_active": "is_active",
            }

            query_filter = {filter_dict[key]: value for key, value in data.items() if
                            key in filter_dict and value is not None}

            if is_active is not None:
                query_filter["is_active"] = is_active

            email_templates = EmailTemplate.objects.filter(**query_filter)

            order_by_dict = {
                "template_type": "template_type",
                "subject": "subject",
            }

            query_order_by = order_by_dict.get(order_by)

            if order_type == "desc" and query_order_by:
                query_order_by = f"-{query_order_by}"

            if query_order_by:
                email_templates = email_templates.order_by(query_order_by)

            paginator = Paginator(email_templates, page_size)
            number_pages = paginator.num_pages

            if page > number_pages and page > 1:
                return Response({"message": "Page not found"}, status=status.HTTP_400_BAD_REQUEST)

            page_obj = paginator.get_page(page)
            results = EmailTemplateReadSerializer(page_obj, many=True)

            return Response({'count': email_templates.count(), 'results': results.data}, status=status.HTTP_200_OK)

        except FieldError as fe:
            print("Error 1")
            return Response({"message": str(fe)}, status=status.HTTP_400_BAD_REQUEST)

        except serializers.ValidationError as ve:
            print("Error 2")
            raise serializers.ValidationError(ve.detail)

        except Exception as ee:
            print("Error 3")
            return Response(str(ee), status=status.HTTP_400_BAD_REQUEST)