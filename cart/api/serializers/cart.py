from rest_framework import serializers

from cart.api.serializers import CartItemSerializer
from cart.models import Cart


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = [
            'id',
            'created_at',
            'expires_at',
            'items',
        ]
