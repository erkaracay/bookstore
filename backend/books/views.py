from rest_framework import generics, permissions
from .models import Book
from .serializers import BookSerializer
from rest_framework.generics import RetrieveAPIView

class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]  # Allow anyone to GET books
        return [permissions.IsAuthenticated()]  # Require auth for POST

class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]  # Allow anyone to GET book details
        return [permissions.IsAuthenticated()]  # Require auth for PUT, DELETE

class BookBySlugView(RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = 'slug'
