from django.db import transaction
from rest_framework.exceptions import ValidationError

from cart.models import CartItem
from products.models import Product
from products.services.product import ProductService


class CartItemService:
    @staticmethod
    def process_cart_item(product: Product, quantity: int, cart) -> None:
        try:
            with transaction.atomic():
                ProductService.reduce_product_inventory(product, quantity)
                CartItem.objects.create(cart=cart, product=product, quantity=quantity)
        except ValidationError as e:
            raise e
