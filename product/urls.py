from django.urls import path
from .views import ProductView

urlpatterns = [
    path('v1/products', ProductView.as_view(), name='product_list_create'),
]
