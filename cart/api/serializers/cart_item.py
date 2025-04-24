from rest_framework import serializers

from cart.models import CartItem


class CartItemSerializer(serializers.ModelSerializer):
    product = serializers.StringRelatedField()

    class Meta:
        model = CartItem
        fields = [
            'product',
            'quantity',
        ]
