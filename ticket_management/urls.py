from django.urls import path
from .views import DepartmentListCreateView, DepartmentRetrieveUpdateDestroyView, SLARetrieveUpdateDestroyAPIView, SLAListCreateAPIView

urlpatterns = [
    path('departments/', DepartmentListCreateView.as_view(), name='department-list-create'),
    path('departments/<int:pk>/', DepartmentRetrieveUpdateDestroyView.as_view(), name='department-detail'),
    path('sla/', SLAListCreateAPIView.as_view(), name='sla-list-create'),
    path('sla/<uuid:pk>/', SLARetrieveUpdateDestroyAPIView.as_view(), name='sla-detail'),
]
