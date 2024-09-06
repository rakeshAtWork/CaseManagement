from drf_spectacular.utils import extend_schema_serializer, OpenApiExample
from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)  # Make id optional for create

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'type', 'description']


class ProductListSerializer(serializers.ListSerializer):
    """This serializer handles the list of products and manages the creation and update logic."""

    def create(self, validated_data):
        """Handles creating new products when id is 0."""
        created_products = []
        for product_data in validated_data:
            if product_data.get('id') == 0:
                product_data.pop('id')  # Remove id before creating a new product
                product = Product.objects.create(**product_data)
                created_products.append(product)
        return created_products

    def update(self, instance, validated_data):
        """Handles updating existing products."""
        updated_products = []
        failed_updates = []

        product_mapping = {product.id: product for product in instance}
        data_mapping = {item['id']: item for item in validated_data if item['id'] != 0}

        for product_id, data in data_mapping.items():
            product = product_mapping.get(product_id)
            if product:
                updated_products.append(self.child.update(product, data))
            else:
                failed_updates.append(product_id)

        return updated_products, failed_updates


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Bulk Create/Update Example',
            summary="Bulk create or update products",
            value=[
                {
                    "id": 0,  # ID 0 for creating new products
                    "name": "New Product - For creating new products id should be 0",
                    "price": 100.00,
                    "type": "Electronics",
                    "description": "A brand new product"
                },
                {
                    "id": 1,  # Existing product ID for updating
                    "name": "Updated Product For updating product id should be other than 0",
                    "price": 150.00,
                    "type": "Toys",
                    "description": "Updated product description"
                }
            ]
        ),
    ]
)
class BulkProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        list_serializer_class = ProductListSerializer  # Use list serializer for batch processing
        fields = ['id', 'name', 'price', 'type', 'description']
