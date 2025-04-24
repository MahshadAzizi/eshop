from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from cart.api.serializers import CartItemSerializer
from cart.selectors.cart import CartSelector
from cart.selectors.cart_item import CartItemSelector
from cart.services.cart_item import CartItemService
from products.services.product import ProductService


class CartItemsView(APIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Get the items in the cart of the logged-in user"""
        cart = CartSelector.get_active_cart(user=request.user)

        if not cart:
            return Response({'detail': 'No active cart found.'}, status=status.HTTP_400_BAD_REQUEST)

        items = CartItemSelector.get_cart_items(cart=cart)
        serializer = CartItemSerializer(items, many=True)
        return Response({
            'cart_id': cart.id,
            'expires_at': cart.expires_at,
            'items': serializer.data
        })

    def post(self, request):
        """Add an item to the cart"""
        cart = CartSelector.get_active_cart(user=request.user)

        if not cart:
            return Response({'detail': 'No active cart found.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product = ProductService.get_product(product_id=request.data.get('product'))
            ProductService.check_product_availability(product, request.data.get('quantity'))
        except ValidationError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        serializer = CartItemSerializer(data=request.data)

        if serializer.is_valid():
            CartItemService.process_cart_item(product=product, quantity=request.data.get('quantity'), cart=cart)

            items = CartItemSelector.get_cart_items(cart=cart)
            serializer = CartItemSerializer(items, many=True)
            return Response({
                'cart_id': cart.id,
                'expires_at': cart.expires_at,
                'items': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
