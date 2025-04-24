from django.urls import path
from cart.api.views import CartView

urlpatterns = [
    path('', CartView.as_view(), name='cart'),
]
