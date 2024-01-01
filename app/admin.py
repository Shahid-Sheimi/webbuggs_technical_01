# app/admin.py
from django.contrib import admin
from .models import ProductCategory, SubCategory, Color, Product

# Register the models directly
admin.site.register(ProductCategory)
admin.site.register(SubCategory)
admin.site.register(Color)
admin.site.register(Product)
