from datetime import timedelta

from django.core.cache import cache
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APITestCase

from cart.models import CartItem, Cart
from products.models import Product
from users.models import User
from cart.tasks import expire_and_deactivate_carts


class CartTestCase(APITestCase):
    def _create_user(self):
        """Helper method to create a user."""
        return User.objects.create_user(phone_number='09121231231', password='123')

    def _create_product_1(self):
        """Helper method to create a product."""
        return Product.objects.create(name='Test Product', inventory=20, price=100.00)

    def _create_product_2(self):
        """Helper method to create a product."""
        return Product.objects.create(name='Test Product 2', inventory=5, price=100.00)

    def setUp(self):
        self.user = self._create_user()
        self.product_1 = self._create_product_1()
        self.product_2 = self._create_product_2()
        self.client.login(phone_number='09121231231', password='123')
        cache.clear()

    def test_get_cart_items(self):
        url = reverse('cart_items')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_can_add_a_to_cart_item(self):
        url = reverse('cart_items')
        data = {
            'product': self.product_1.id,
            'quantity': 2
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)

        cart_item = CartItem.objects.first()
        self.assertEqual(cart_item.product, self.product_1)
        self.assertEqual(cart_item.quantity, 2)

        self.product_1.refresh_from_db()
        self.assertEqual(self.product_1.inventory, 18)

    def test_add_to_cart_with_insufficient_stock(self):
        url = reverse('cart_items')
        data = {
            'product': self.product_1.id,
            'quantity': 22
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('Not enough stock', response.data['detail'])

        self.assertEqual(CartItem.objects.count(), 0)

        self.product_1.refresh_from_db()
        self.assertEqual(self.product_1.inventory, 20)

    def test_celery_task(self):
        """Test that a task runs and returns the expected result."""

        url = reverse('cart_items')
        data_1 = {
            'product': self.product_1.id,
            'quantity': 3
        }

        data_2 = {
            'product': self.product_2.id,
            'quantity': 3
        }

        response_1 = self.client.post(url, data_1, format='json')
        self.product_1.refresh_from_db()
        self.assertEqual(self.product_1.inventory, 17)

        _ = self.client.post(url, data_2, format='json')
        self.product_2.refresh_from_db()
        self.assertEqual(self.product_2.inventory, 2)

        cart = Cart.objects.get(id=response_1.data.get('cart_id'))
        cart.expires_at = timezone.now() - timedelta(seconds=1)
        cart.save()

        task = expire_and_deactivate_carts.apply()
        cart.refresh_from_db()
        self.product_1.refresh_from_db()
        self.product_2.refresh_from_db()

        self.assertEqual(cart.is_active, False)
        self.assertEqual(self.product_1.inventory, 20)
        self.assertEqual(self.product_2.inventory, 5)
