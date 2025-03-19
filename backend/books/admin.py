from django.contrib import admin
from .models import Book

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'price', 'stock', 'published_date', 'slug')
    search_fields = ('title', 'author', 'slug')

admin.site.register(Book, BookAdmin)