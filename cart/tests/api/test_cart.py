from django.urls import reverse
from rest_framework.test import APITestCase

from products.models import Product
from users.models import User


class CartTestCase(APITestCase):
    def _create_user(self):
        """Helper method to create a user."""
        return User.objects.create_user(phone_number='09121231231', password='123')

    def _create_product(self):
        """Helper method to create a product."""
        return Product.objects.create(name='Test Product', inventory=20, price=100.00)

    def setUp(self):
        self.user = self._create_user()
        self.product = self._create_product()
        self.client.login(phone_number='09121231231', password='123')

    def test_cart(self):
        url = reverse('cart')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_cart_without_authentication(self):
        self.client.logout()
        url = reverse('cart')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

