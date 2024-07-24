from rest_framework import generics
from .models import Department, SLA
from .serializers import DepartmentSerializer, SLASerializer


class DepartmentListCreateView(generics.ListCreateAPIView):
    queryset = Department.objects.filter(is_active=True, is_delete=False)
    serializer_class = DepartmentSerializer


class DepartmentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Department.objects.filter(is_active=True, is_delete=False)
    serializer_class = DepartmentSerializer


class SLAListCreateAPIView(generics.ListCreateAPIView):
    queryset = SLA.objects.all()
    serializer_class = SLASerializer


class SLARetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SLA.objects.all()
    serializer_class = SLASerializer
