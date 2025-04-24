from typing import Optional

from cart.models import CartItem


class CartItemSelector:
    @staticmethod
    def get_cart_items(cart) -> Optional[CartItem]:
        return CartItem.objects.select_related('product').filter(cart=cart)
