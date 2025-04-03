from rest_framework import generics, permissions, status
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from .models import Book
from .serializers import BookSerializer
from users.permissions import IsAdminOrSeller
from django.utils.decorators import method_decorator
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from django.utils.encoding import iri_to_uri
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

@method_decorator(cache_page(30), name='dispatch')
class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [IsAdminOrSeller()]

    @swagger_auto_schema(
        operation_description="Retrieve a list of books or create a new book.",
        responses={200: BookSerializer(many=True), 201: BookSerializer, 400: "Validation Error"},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Create a new book or multiple books.",
        request_body=BookSerializer(many=True),
        responses={201: BookSerializer(many=True), 400: "Validation Error"},
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        is_many = isinstance(request.data, list)
        serializer = self.get_serializer(data=request.data, many=is_many)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

@method_decorator(cache_page(30), name='dispatch')
class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    @swagger_auto_schema(
        operation_description="Retrieve a book by ID.",
        responses={200: BookSerializer, 404: "Not Found"},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update a book by ID.",
        request_body=BookSerializer,
        responses={200: BookSerializer, 400: "Validation Error", 404: "Not Found"},
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Delete a book by ID.",
        responses={204: "No Content", 404: "Not Found"},
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

    def perform_update(self, serializer):
        instance = serializer.save()
        # Invalidate cache for this specific book URL
        cache_key = iri_to_uri(self.request.build_absolute_uri())
        cache.delete(cache_key)

    def perform_destroy(self, instance):
        cache_key = iri_to_uri(self.request.build_absolute_uri())
        cache.delete(cache_key)
        instance.delete()

class BookBySlugView(RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = 'slug'

    @swagger_auto_schema(
        operation_description="Retrieve a book by slug.",
        responses={200: BookSerializer, 404: "Not Found"},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

@api_view(['POST'])
@permission_classes([IsAdminUser])
@swagger_auto_schema(
    operation_description="Clear all cached book data.",
    responses={200: "Cache cleared successfully."},
)
def clear_all_book_cache(request):
    cache.clear()
    return Response({"detail": "All book cache cleared."})