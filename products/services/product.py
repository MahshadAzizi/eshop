import logging
from typing import Optional

from django.core.cache import cache
from django.db import transaction
from rest_framework.exceptions import ValidationError

from cart.models import CartItem
from products.models import Product

logger = logging.getLogger('product')


class ProductService:
    @staticmethod
    def get_product(product_id: int) -> Optional[Product]:
        try:
            return Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            logger.error('Product not found.')
            raise ValidationError('Product not found.')

    @staticmethod
    def check_product_availability(product: Product, quantity: int):
        """Check if the product is available in the requested quantity."""
        product_key = f'product_{product.id}_inventory'
        available_stock = cache.get(product_key)
        if available_stock is None:
            available_stock = product.inventory
            cache.set(product_key, available_stock, timeout=60 * 60)

        if available_stock < quantity:
            raise ValidationError(
                f'Not enough stock for product {product.name}. Available: {product.inventory}, Requested: {quantity}')

        if not product.is_active:
            raise ValidationError(
                f'The product is not available.')
        return True

    @staticmethod
    def reduce_product_inventory(product: Product, quantity: int) -> None:
        """Reduce the product's inventory by the given quantity."""
        product_key = f'product_{product.id}_inventory'

        with transaction.atomic():
            product = Product.objects.select_for_update().get(id=product.id)

            available_stock = cache.get(product_key)

            if available_stock < quantity:
                logger.warning(
                    f'Not enough stock for product {product.name} (ID: {product.id}). '
                    f'Available: {available_stock}, Requested: {quantity}.')
                raise ValidationError(
                    f'Not enough stock for product {product.name}. Available: {available_stock}, Requested: {quantity}')

            if available_stock is None:
                available_stock = product.inventory
                cache.set(product_key, available_stock, timeout=60 * 60)
                logger.info(f'Cache miss for product {product.name}, loading from database.')

            available_stock -= quantity
            if available_stock <= 0:
                product.product_deactivated()
                cache.delete(product_key)
                logger.info(f'Product {product.name} (ID: {product.id}) is now deactivated due to zero stock.')

            else:
                cache.set(product_key, available_stock)

            product.reduce_inventory(quantity)

            logger.info(
                f'Inventory for product {product.name} (ID: {product.id}) reduced by {quantity}. New inventory: {product.inventory}.')

    @staticmethod
    def restore_product_inventory(cart):
        """Restore the inventory for the products in the expired cart."""
        cart_items = CartItem.objects.filter(cart=cart)
        for item in cart_items:
            product = item.product

            with transaction.atomic():
                product = Product.objects.select_for_update().get(id=product.id)

                product.restore_inventory(item.quantity)

                product_key = f'product_{product.id}_inventory'
                available_stock = cache.get(product_key)

                if available_stock is not None:
                    new_stock = available_stock + item.quantity
                    cache.set(product_key, new_stock)
                else:
                    new_stock = product.inventory
                    cache.set(product_key, new_stock, timeout=60 * 60)

                if new_stock <= 0:
                    product.product_deactivated()
                    cache.delete(product_key)
                else:
                    product.product_activate()
