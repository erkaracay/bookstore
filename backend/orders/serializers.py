from rest_framework import serializers
from .models import Order, OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['book', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'created_at', 'status', 'total_price', 'items']
        read_only_fields = ['id', 'user', 'created_at', 'status', 'total_price']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(user=self.context['request'].user)
        total = 0

        for item in items_data:
            book = item['book']
            quantity = item['quantity']

            if book.stock < quantity:
                raise serializers.ValidationError(f"Not enough stock for '{book.title}'")

            book.stock -= quantity
            book.save()
            OrderItem.objects.create(order=order, book=book, quantity=quantity)
            total += book.price * quantity

        order.total_price = total
        order.save()

        return order

class OrderStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['status']
