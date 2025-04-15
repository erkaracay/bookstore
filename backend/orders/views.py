from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from .models import Order
from .serializers import OrderSerializer, OrderStatusUpdateSerializer
from users.permissions import IsOwnerOrAdmin
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

VALID_TRANSITIONS = {
    'pending': ['shipped', 'cancelled'],
    'shipped': [],
    'cancelled': [],
}

class OrderListView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Get a list of your past orders. Orders are created via cart checkout only.",
        responses={200: OrderSerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.groups.filter(name__iexact='admin').exists():
            return Order.objects.all()
        return Order.objects.filter(user=user)

    @swagger_auto_schema(
        operation_description="❌ Disabled. Use /cart/checkout/ to create orders.",
        request_body=openapi.Schema(type=openapi.TYPE_OBJECT),
        responses={400: "Manual order creation is not allowed."}
    )
    def post(self, request, *args, **kwargs):
        raise ValidationError("Orders must be created via /cart/checkout/. Manual creation is not allowed.")


class OrderDetailView(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]

    @swagger_auto_schema(
        operation_description="Retrieve details of a specific order by ID.",
        responses={200: OrderSerializer, 404: "Not Found"},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class OrderStatusUpdateView(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderStatusUpdateSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]

    @swagger_auto_schema(
        operation_description="Update the status of an order (admin only for shipping).",
        request_body=OrderStatusUpdateSerializer,
        responses={200: OrderStatusUpdateSerializer, 400: "Invalid transition", 403: "Forbidden"},
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        order = self.get_object()
        new_status = request.data.get('status')
        current_status = order.status

        if new_status not in VALID_TRANSITIONS.get(current_status, []):
            return Response(
                {"detail": f"Invalid status transition from {current_status} to {new_status}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if new_status == 'shipped' and not request.user.groups.filter(name__iexact='admin').exists():
            return Response(
                {"detail": "Only admins can mark an order as shipped."},
                status=status.HTTP_403_FORBIDDEN
            )

        return super().update(request, *args, **kwargs)


class CancelOrderView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]

    @swagger_auto_schema(
        operation_description="Cancel an order (only if pending). Use with caution — legacy or admin only.",
        responses={200: "Order cancelled successfully.", 400: "Invalid", 404: "Not Found"},
    )
    def post(self, request, pk):
        try:
            order = Order.objects.get(pk=pk, user=request.user)
        except Order.DoesNotExist:
            return Response({"detail": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

        if order.status != "pending":
            return Response({"detail": "Only pending orders can be cancelled."}, status=status.HTTP_400_BAD_REQUEST)

        # Restore stock
        for item in order.items.all():
            book = item.book
            book.stock += item.quantity
            book.save()

        order.status = "cancelled"
        order.save()

        return Response({"detail": "Order cancelled and stock restored."}, status=status.HTTP_200_OK)
