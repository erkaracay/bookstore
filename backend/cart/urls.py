from django.urls import path
from .views import (
    CartView, CartItemCreateView, CartItemUpdateDeleteView, CartCheckoutView
)

urlpatterns = [
    path('', CartView.as_view(), name='cart-view'),
    path('items/', CartItemCreateView.as_view(), name='cart-item-create'),
    path('items/<int:pk>/', CartItemUpdateDeleteView.as_view(), name='cart-item-update-delete'),
    path('checkout/', CartCheckoutView.as_view(), name='cart-checkout'),
]
