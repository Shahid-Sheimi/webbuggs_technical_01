# accounts/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    contact_number = models.CharField(max_length=15, null=True, blank=True)
    USER_ROLES = (
        ('C', 'Customer'),
        ('S', 'Seller')
    )
    user_role = models.CharField(max_length=1, choices=USER_ROLES, default='C')  
    email = models.EmailField(("email address"), unique=True)

    def __str__(self):
        return f"{self.username}"
    
    @property
    def product_count(self):
        return self.products_uploaded.count()



