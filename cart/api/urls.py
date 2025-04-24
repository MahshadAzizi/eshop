from django.urls import path
from cart.api.views import CartView, CartItemsView

urlpatterns = [
    path('', CartView.as_view(), name='cart'),
    path('items', CartItemsView.as_view(), name='cart_items')
]
