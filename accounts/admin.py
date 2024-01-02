# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    list_display = [
        'username',
        'first_name',
        'last_name',
        'email',
        'is_superuser',
        'date_joined',
        'is_staff',
        'is_active',
        'last_login',
    ]
    search_fields = ['username', 'email', 'first_name', 'last_name']
    list_filter = ['is_staff', 'is_active']

    # Customize the order and visibility of the fields in the detail view
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email', 'contact_number')}),
        ('Permissions', {'fields': ('is_superuser', 'is_staff', 'is_active')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    readonly_fields = ['date_joined', 'last_login']

# Register the CustomUser model with the custom admin class
admin.site.register(CustomUser, CustomUserAdmin)
