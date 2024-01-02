# app/models.py
from django.db import models
from accounts.models import CustomUser
from django.contrib.auth import get_user_model
from django.db import models

class ProductCategory(models.Model):
    name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='category_images/', null=True, blank=True)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='product_categories_created')
    updated_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='product_categories_updated')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
class SubCategory(models.Model):
    name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='subcategory_images/', null=True, blank=True)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='subcategories_created')
    updated_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='subcategories_updated')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
class Color(models.Model):
    name = models.CharField(max_length=50)
    color_code = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)  # Add this line
    def __str__(self):
        return self.name
class Product(models.Model): 
    title = models.CharField(max_length=100)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name='products')
    # category = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    description = models.TextField()
    sku = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='products_uploaded')
    updated_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='products_updated')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    colors = models.ManyToManyField(Color)
    def save(self, *args, **kwargs):
        # Generate SKU before saving
        if not self.sku:
            self.sku = f"prod-{self.created_at.strftime('%Y%m%d')}-{self.id}"
        super().save(*args, **kwargs)
class SoftDeletionManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)
class Product(models.Model):
    name = models.CharField(max_length=255, default="Unknown")
    description = models.TextField()
    is_deleted = models.BooleanField(default=False)
    objects = SoftDeletionManager()
    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.save()
    def __str__(self):
        return self.product_name
    # Other fields...
    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.save()
