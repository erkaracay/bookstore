from django.urls import path
from .views import BookListCreateView, BookDetailView, BookBySlugView, clear_all_book_cache

urlpatterns = [
    path('', BookListCreateView.as_view(), name='book-list-create'),
    path('<int:pk>/', BookDetailView.as_view(), name='book-detail'),  # Fetch by ID
    path('<str:slug>/', BookBySlugView.as_view(), name='book-detail-by-slug'),  # Fetch by Slug
    path('clear-cache/', clear_all_book_cache, name='clear-book-cache'),
]
