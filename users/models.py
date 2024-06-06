from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class CustomUser(AbstractUser):
    is_buyer = models.BooleanField(default=False, null=False, blank=False)
    is_seller = models.BooleanField(default=False, null=False, blank=False)
    email = models.EmailField(unique=True, null=False, blank=False)
    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )


    def __str__(self):
        return self.username


class Address(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='addresses')
    seller = models.ForeignKey(
        'SellerProfile', 
        on_delete=models.CASCADE, 
        related_name='store_addresses', 
        null=True, 
        blank=True
    )
    street_address = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    postal_code = models.CharField(max_length=20, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    primary = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.street_address}"


class BuyerProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='buyer_profile')
    phone_number = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return self.user.username


class SellerProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='seller_profile')
    store_name = models.CharField(max_length=255)
    store_description = models.TextField(null=True, blank=True)
    store_address = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.store_name
