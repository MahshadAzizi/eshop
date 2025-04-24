from django.core.cache import cache

from cart.models import Cart


class CartService:
    @staticmethod
    def create_cart_for_user(user):
        """Create a new active cart for a given user with a 30-minute expiration."""
        cart = Cart.objects.create(user=user)
        cart_key = f'cart_{user.id}_active'
        cache.set(cart_key, cart, timeout=1800)
        return cart
