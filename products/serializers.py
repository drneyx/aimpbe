from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    region = serializers.StringRelatedField()
    district = serializers.StringRelatedField()
    
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'sku', 'seller', 'category', 'description', 'price', 
            'stock_quantity', 'stock_status', 'status', 'region', 'district', 
            'latitude', 'longtude', 'available', 'published', 'created_at', 
            'updated_at', 'image', 'image_cdn', 'slug'
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['price'] = int(float(instance.price) * 100)  # Convert to integer cents
        return representation