from rest_framework import serializers
from .models import Order, OrderItem
from books.models import Book
from books.serializers import SimpleBookSerializer

class OrderItemSerializer(serializers.ModelSerializer):
    book = SimpleBookSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['book', 'quantity', 'price']

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be at least 1.")
        return value

    def validate(self, attrs):
        book = attrs.get('book')
        quantity = attrs.get('quantity')
        if book and quantity and book.stock < quantity:
            raise serializers.ValidationError(f"Not enough stock for '{book.title}'. Only {book.stock} available.")
        return attrs

class OrderSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'created_at', 'status', 'total_price', 'items']
        read_only_fields = ['id', 'user', 'created_at', 'status', 'total_price']

    def create(self, validated_data):
        items_data = self.initial_data.get('items')

        if not items_data:
            raise serializers.ValidationError("Order must contain at least one item.")

        order = Order.objects.create(user=self.context['request'].user)
        total = 0

        for item in items_data:
            book = Book.objects.get(id=item['book'])
            quantity = item['quantity']

            if book.stock < quantity:
                raise serializers.ValidationError(f"Not enough stock for '{book.title}'")

            book.stock -= quantity
            book.save()

            OrderItem.objects.create(
                order=order,
                book=book,
                quantity=quantity,
                price=book.price
            )

            total += book.price * quantity

        order.total_price = total
        order.save()

        return order

class OrderStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['status']

    def validate_status(self, value):
        instance = self.instance

        if instance.status == 'shipped' and value not in ['shipped']:
            raise serializers.ValidationError("A shipped order cannot be updated to any other status.")

        if instance.status == 'cancelled' and value not in ['cancelled']:
            raise serializers.ValidationError("A cancelled order cannot be updated.")

        return value
