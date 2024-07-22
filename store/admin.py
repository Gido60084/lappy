# Register your models here.
from django.contrib import admin
from .models import Category, Product, Cart, CartItem, Order, OrderItem
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'stock', 'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated', 'category']
    list_editable = ['price', 'stock', 'available']


class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at']

class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'product', 'quantity', 'created_at']

class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'total_amount', 'created_at']

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'price']


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)