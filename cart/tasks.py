import logging

from celery import shared_task
from django.core.cache import cache
from django.utils import timezone

from cart.models import Cart
from products.services.product import ProductService

logger = logging.getLogger('celery')


@shared_task
def expire_and_deactivate_carts():
    """Task that checks for expired carts and deactivates them in the database and cache."""
    expired_carts = Cart.objects.filter(is_active=True, expires_at__lt=timezone.now())
    logger.info('start celery task')
    for cart in expired_carts:
        ProductService.restore_product_inventory(cart)

        cart.cart_deactivate()
        cache.delete(f'cart_{cart.user.id}_active')

        logger.info(f'Deactivated cart for user {cart.user.id} and removed from cache.')
