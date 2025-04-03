from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Order
from .serializers import OrderSerializer, OrderStatusUpdateSerializer
from users.permissions import IsOwnerOrAdmin

VALID_TRANSITIONS = {
    'pending': ['shipped', 'cancelled'],
    'shipped': [],
    'cancelled': [],
}

class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

def get_queryset(self):
    user = self.request.user
    if user.is_superuser or user.groups.filter(name='Admin').exists():
        return Order.objects.all()
    return Order.objects.filter(user=user)

    def perform_create(self, serializer):
        # When creating an order, associate the logged-in user with the order
        serializer.save(user=self.request.user)

class OrderDetailView(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]

class OrderStatusUpdateView(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderStatusUpdateSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]

    def update(self, request, *args, **kwargs):
        order = self.get_object()
        new_status = request.data.get('status')
        current_status = order.status

        if new_status not in VALID_TRANSITIONS.get(current_status, []):
            return Response(
                {"detail": f"Invalid status transition from {current_status} to {new_status}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if new_status == 'shipped' and not request.user.groups.filter(name='Admin').exists():
            return Response(
                {"detail": "Only admins can mark an order as shipped."},
                status=status.HTTP_403_FORBIDDEN
            )

        return super().update(request, *args, **kwargs)

class CancelOrderView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]

    def post(self, request, pk):
        try:
            order = Order.objects.get(pk=pk, user=request.user)
        except Order.DoesNotExist:
            return Response({"detail": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

        if order.status != "pending":
            return Response({"detail": "Only pending orders can be cancelled."}, status=status.HTTP_400_BAD_REQUEST)

        for item in order.items.all():
            book = item.book
            book.stock += item.quantity
            book.save()

        order.status = "cancelled"
        order.save()

        return Response({"detail": "Order cancelled and stock restored."}, status=status.HTTP_200_OK)
