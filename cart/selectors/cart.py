from typing import Optional

from cart.models import Cart


class CartSelector:
    @staticmethod
    def get_active_cart(user) -> Optional[Cart]:
        return Cart.objects.filter(user=user, is_active=True).first()

