from django.contrib import admin
from .models import CustomUser, Address, BuyerProfile, SellerProfile

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_buyer', 'is_seller', 'is_staff')
    search_fields = ('username', 'email')
    list_filter = ('is_buyer', 'is_seller', 'is_staff')


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'street_address', 'city', 'state', 'postal_code', 'country', 'primary')
    search_fields = ('user__username', 'street_address', 'city', 'state', 'postal_code', 'country')
    list_filter = ('primary',)

@admin.register(BuyerProfile)
class BuyerProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('user__username',)


@admin.register(SellerProfile)
class SellerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'store_name', 'approved')
    search_fields = ('user__username', 'store_name')
    list_filter = ('approved',)