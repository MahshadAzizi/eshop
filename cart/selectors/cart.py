from typing import Optional

from django.core.cache import cache
from django.utils import timezone

from cart.models import Cart


class CartSelector:
    @staticmethod
    def get_active_cart(user) -> Optional[Cart]:
        cart_key = f'cart_{user.id}_active'
        cart = cache.get(cart_key)
        if cart:
            return cart

        cart = Cart.objects.filter(user=user, is_active=True).first()
        if cart:
            if cart.expires_at <= timezone.now():
                cart.cart_deactivate()
                cache.delete(cart_key)
                return None

            ttl = (cart.expires_at - timezone.now()).total_seconds()
            cache.set(cart_key, cart, timeout=ttl)
        return cart
