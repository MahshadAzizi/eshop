from cart.models import Cart


class CartService:
    @staticmethod
    def create_cart_for_user(user):
        """Create a new active cart for a given user with a 30-minute expiration."""
        return Cart.objects.create(
            user=user,
        )
