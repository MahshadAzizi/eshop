from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from cart.api.serializers import CartSerializer
from cart.selectors.cart import CartSelector
from cart.services.cart import CartService


class CartView(APIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart = CartSelector.get_active_cart(user=request.user)

        if not cart:
            cart = CartService.create_cart_for_user(request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)
