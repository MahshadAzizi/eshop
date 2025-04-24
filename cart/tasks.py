from celery import shared_task
from django.core.cache import cache
from django.utils import timezone

from cart.models import Cart


@shared_task
def expire_and_deactivate_carts():
    """Task that checks for expired carts and deactivates them in the database and cache."""
    expired_carts = Cart.objects.filter(is_active=True, expires_at__lt=timezone.now())

    for cart in expired_carts:
        cart.cart_deactivate()
        cache.delete(f'cart_{cart.user.id}_active')

        print(f"Deactivated cart for user {cart.user.id} and removed from cache.")