# app/views.py
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from .models import ProductCategory, SubCategory, Color, Product,CustomUser
from .serializers import ProductCategorySerializer, SubCategorySerializer, ColorSerializer, ProductSerializer,ProductFilterSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count
from .models import ProductCategory, Product
from .serializers import ProductCategorySerializer,UserProductInfoSerializer
from django.db import models
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count
from .models import ProductCategory
from rest_framework.permissions import AllowAny
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import PageNumberPagination
from app.permissions import IsAdminUserOrReadOnly


class TopCategoriesView(APIView):
    def get(self, request, *args, **kwargs):
        # Query to get the top 3 categories with the highest number of products
        top_categories = ProductCategory.objects.annotate(product_count=Count('products')).order_by('-product_count')[:3]
        # Serialize the result
        serializer = ProductCategorySerializer(top_categories, many=True)
        return Response(serializer.data)

class ProductCategoryUpdateView(generics.UpdateAPIView):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
    permission_classes = [permissions.AllowAny]

class SubCategoryUpdateView(generics.UpdateAPIView):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer
    permission_classes = [permissions.AllowAny]

class ColorUpdateView(generics.UpdateAPIView):
    queryset = Color.objects.all()
    serializer_class = ColorSerializer
    permission_classes = [permissions.AllowAny]

class ProductUpdateView(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]

# ProductCategory views
class ProductCategoryListView(generics.ListCreateAPIView):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
    permission_classes = [permissions.AllowAny]

class ProductCategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
    permission_classes = [permissions.AllowAny]

class ProductCategoryUpdateView(generics.UpdateAPIView):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
    permission_classes = [permissions.AllowAny]

class ProductCategoryDeleteView(generics.DestroyAPIView):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
    permission_classes = [permissions.AllowAny]

class ProductListPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class ProductListView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        filtered_data = [{'title': item['title'], 'description': item['description'], 'sku': item['sku'], 'category': item['category']} for item in data]
        return Response(filtered_data)

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]

class ProductUpdateView(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]

class ProductDeleteView(generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]
    
class SubCategoryListView(generics.ListCreateAPIView):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        # Set the created_by and updated_by fields before saving a new instance
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

    def list(self, request, *args, **kwargs):
        # Overriding list method to set updated_by for all instances before listing
        queryset = self.get_queryset()
        for instance in queryset:
            instance.updated_by = self.request.user
            instance.save()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
class SubCategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer
    permission_classes = [permissions.AllowAny]

    def perform_update(self, serializer):
        # Set the updated_by field before updating an instance
        serializer.save(updated_by=self.request.user)

    def perform_destroy(self, instance):
        # Soft delete by setting is_active to False
        instance.is_active = False
        instance.updated_by = self.request.user
        instance.save()

class SubCategoryDeleteView(generics.DestroyAPIView):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer
    permission_classes = [permissions.AllowAny]

    def perform_destroy(self, instance):
        # Soft delete by setting is_active to False
        instance.is_active = False
        instance.updated_by = self.request.user
        instance.save()       
class ColorListView(generics.ListCreateAPIView):
    
    queryset = Color.objects.filter(is_active=True)
    serializer_class = ColorSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        # Set the created_by and updated_by fields
        serializer.save(created_by=self.request.user, updated_by=self.request.user)        
class ColorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Color.objects.all()
    serializer_class = ColorSerializer
    permission_classes = [permissions.AllowAny]

class ColorDeleteView(generics.DestroyAPIView):
    queryset = Color.objects.all()
    serializer_class = ColorSerializer
    permission_classes = [permissions.AllowAny]

class TopCategoriesView(APIView):
    def get(self, request, *args, **kwargs):
        # Query to get the top 3 categories with the highest number of products
        top_categories = ProductCategory.objects.annotate(product_count=Count('products')).order_by('-product_count')[:3]
        # Serialize the result
        serializer = ProductCategorySerializer(top_categories, many=True)
        return Response(serializer.data)
class ProductFilterView(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        # Get the filter parameters from the request
        serializer = ProductFilterSerializer(data=self.request.query_params)
        serializer.is_valid(raise_exception=True)
        keyword = serializer.validated_data.get('keyword', '')
        sku = serializer.validated_data.get('sku', '')

        # Filter products based on the keyword and sku
        queryset = Product.objects.filter(
            title__icontains=keyword,
            description__icontains=keyword,
            sku__icontains=sku,
        )
        return queryset
class UserProductInfoView(generics.RetrieveAPIView):
    serializer_class = UserProductInfoSerializer
    queryset = CustomUser.objects.all()
    def retrieve(self, request, *args, **kwargs):
        user = self.get_object()
        product_count = Product.objects.filter(created_by=user).count()

        serializer = self.get_serializer(user)
        response_data = serializer.data
        response_data['product_count'] = product_count
        return Response(response_data)

class ProductListPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class ProductListView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = ProductListPagination

class ProductDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]







































