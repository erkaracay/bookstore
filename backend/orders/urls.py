from django.urls import path
from .views import OrderListView, OrderDetailView, OrderStatusUpdateView, CancelOrderView

urlpatterns = [
    path('', OrderListView.as_view(), name='order-list-create'),
    path('<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('<int:pk>/status/', OrderStatusUpdateView.as_view(), name='order-status-update'),
    path('<int:pk>/cancel/', CancelOrderView.as_view(), name='order-cancel'),
]