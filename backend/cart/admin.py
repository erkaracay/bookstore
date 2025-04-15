from django.contrib import admin
from .models import Cart, CartItem

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ['book', 'quantity']

class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'created_at']
    inlines = [CartItemInline]
    search_fields = ['user__email', 'user__username']

admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem)
