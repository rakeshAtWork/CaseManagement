from drf_spectacular.utils import extend_schema, OpenApiExample
from rest_framework import generics, status
from rest_framework.response import Response
from .models import Product
from .serializers import BulkProductSerializer, ProductSerializer


class ProductView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = BulkProductSerializer

    @extend_schema(
        request=BulkProductSerializer(many=True),  # Uses the decorated serializer
    )
    def create(self, request, *args, **kwargs):
        products_data = request.data
        # Check if the payload is a single object and wrap it in a list if necessary
        # if isinstance(products_data, dict):
        #     products_data = [products_data]

        if not isinstance(products_data, list):
            return Response(
                {"error": "Invalid data format. Expected a list of products or a single product object in a List."},
                status=status.HTTP_400_BAD_REQUEST
            )
        created_records = []
        updated_records = []
        failed_updates = []

        for product_data in products_data:
            product_id = product_data.get('id', None)

            if product_id == 0:
                # Create new record if id is 0
                serializer = self.get_serializer(data=product_data)
                serializer.is_valid(raise_exception=True)
                self.perform_create(serializer)
                created_records.append(serializer.data)
            else:
                try:
                    # Try to update existing record if id is present
                    product = Product.objects.get(id=product_id)
                    serializer = self.get_serializer(product, data=product_data)
                    serializer.is_valid(raise_exception=True)
                    serializer.save()
                    updated_records.append(serializer.data)
                except Product.DoesNotExist:
                    # If product with the id doesn't exist, add to failed updates
                    failed_updates.append({"id": product_id, "status": "Update failed, product does not exist"})

        return Response(
            {
                'created': created_records,
                'updated': updated_records,
                'failed_updates': failed_updates
            },
            status=status.HTTP_200_OK
        )
