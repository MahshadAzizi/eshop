from typing import Optional

from rest_framework.exceptions import ValidationError

from products.models import Product


class ProductService:
    @staticmethod
    def get_product(product_id: int) -> Optional[Product]:
        try:
            return Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise ValidationError('Product not found.')

    @staticmethod
    def check_product_availability(product: Product, quantity: int) -> bool:
        """Check if the product is available in the requested quantity."""
        if product.inventory < quantity:
            raise ValidationError(
                f'Not enough stock for product {product.name}. Available: {product.inventory}, Requested: {quantity}')

    @staticmethod
    def reduce_product_inventory(product: Product, quantity: int) -> None:
        """Reduce the product's inventory by the given quantity."""
        product.reduce_inventory(quantity)
