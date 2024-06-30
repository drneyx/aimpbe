from django.contrib import admin

from users.models import CustomUser
from .models import Category, Product,  Order, OrderItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'slug')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'available', 'created_at', 'updated_at')
    list_filter = ('category', 'available', 'created_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}

# # Customer admin
# @admin.register(CustomUser)
# class CustomerAdmin(admin.ModelAdmin):
#     list_display = ('first_name', 'last_name', 'email', 'phone')
#     search_fields = ('first_name', 'last_name', 'email', 'phone')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'total', 'status', 'created_at', 'updated_at')
    list_filter = ('status', 'created_at')
    search_fields = ('customer__first_name', 'customer__last_name', 'customer__email')


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price')
    search_fields = ('order__id', 'product__name')
