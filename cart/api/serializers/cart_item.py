from rest_framework import serializers

from cart.models import CartItem
from products.api.serializers import ProductSerializer
from products.models import Product


class CartItemSerializer(serializers.ModelSerializer):
    product = serializers.SlugRelatedField(queryset=Product.objects.all(), slug_field='id', write_only=True)
    product_detail = ProductSerializer(source='product', read_only=True)

    class Meta:
        model = CartItem
        fields = [
            'product',
            'product_detail',
            'quantity',
        ]
