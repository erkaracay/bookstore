from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        seller = serializers.ReadOnlyField(source='seller.email')
        fields = ['id', 'title', 'slug', 'author', 'price', 'stock', 'description', 'published_date', 'seller']
        read_only_fields = ['slug']

    def validate_title(self, value):
        qs = Book.objects.filter(title__iexact=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("A book with this title already exists.")
        return value

    def validate(self, attrs):
        if attrs.get('price', 0) <= 0:
            raise serializers.ValidationError("Price must be greater than 0.")
        if attrs.get('stock', 0) < 0:
            raise serializers.ValidationError("Stock cannot be negative.")
        return attrs

class SimpleBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title']
