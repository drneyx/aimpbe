from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from dashboard.models import District, Region

from users.models import CustomUser


STATUS = [
    ('DRAFT', _('draft')),
    ('PUBLISHED', _('published')),
]

STOCK_STATUS_CHOICES = [
    ('IN STOCK', _('In Stock')),
    ('OUT OF STOCK', _('Out of Stock')),
]


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcategories')
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=15, choices=STATUS, null=True, blank=True, default='DRAFT')

    class Meta:
        indexes = [
            models.Index(fields=['slug']),
        ]
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)


class Product(models.Model):
    name = models.CharField(max_length=255)
    sku = models.CharField(blank=True, null=True)
    seller = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='orders', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='sproducts', null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.IntegerField()
    stock_status = models.CharField(max_length=15, choices=STOCK_STATUS_CHOICES, null=True, blank=True, default='OUT OF STOCK')
    status = models.CharField(max_length=15, choices=STATUS, null=True, blank=True, default='DRAFT')
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, related_name='region_products', blank=True, null=True)
    district =  models.ForeignKey(District, on_delete=models.SET_NULL, related_name='districts_products', blank=True, null=True)
    latitude = models.CharField(max_length=255, null=True, blank=True)
    longtude = models.CharField(max_length=255, null=True, blank=True)
    available = models.BooleanField(default=True)
    published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    image_cdn = models.CharField(blank=True, null=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['slug']),
        ]
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)


class Order(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='corders')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    STATUS_CHOICES = [
        ('PENDING', _('Pending')),
        ('PROCESSING', _('Processing')),
        ('SHIPPED', _('Shipped')),
        ('DELIVERED', _('Delivered')),
        ('CANCELLED', _('Cancelled')),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Order {self.id} - {self.customer.first_name} {self.customer.last_name}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f'{self.quantity} x {self.product.name}'

    def get_total_price(self):
        return self.quantity * self.price
