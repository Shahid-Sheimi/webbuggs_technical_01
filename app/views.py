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


class TopCategoriesView(APIView):
    def get(self, request, *args, **kwargs):
        top_categories = ProductCategory.objects.annotate(product_count=Count('products_uploaded')).order_by('-product_count')[:3]
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
        # Check if the user is authenticated
        if self.request.user.is_authenticated:
            # Check if the user is a valid instance of CustomUser
            if not isinstance(self.request.user, CustomUser):
                raise ValueError("Invalid user type for created_by field. Must be a CustomUser instance.")
            
            serializer.save(created_by=self.request.user, updated_by=self.request.user)
        else:
            # Handle the case of an anonymous user (optional)
            serializer.save(created_by=None, updated_by=None)

    def list(self, request, *args, **kwargs):
        # Overriding list method to set updated_by for all instances before listing
        queryset = self.get_queryset()
        
        for instance in queryset:
            # Ensure that the user is a CustomUser instance before updating
            if isinstance(self.request.user, CustomUser):
                instance.updated_by = self.request.user
                instance.save()

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    
class SubCategoryDetailView(generics.CreateAPIView, generics.RetrieveUpdateDestroyAPIView):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer

    def perform_create(self, serializer):
        # Set the creator to the authenticated user or None if anonymous
        created_by = self.request.user if self.request.user.is_authenticated else None

        # If the user is authenticated, ensure it's a CustomUser instance
        if created_by and not isinstance(created_by, CustomUser):
            raise ValueError("Invalid user type for created_by field")

        serializer.save(created_by=created_by)

    def create(self, request, *args, **kwargs):
        # If the user is authenticated, ensure it's a CustomUser instance
        if self.request.user.is_authenticated and not isinstance(self.request.user, CustomUser):
            raise ValueError("Invalid user type for created_by field")

        return super().create(request, *args, **kwargs)
    
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

class ProductFilterView(APIView):
    def get(self, request, *args, **kwargs):
        # Get the 'sku' parameter from the request's query parameters
        sku_param = request.query_params.get('sku', None)

        if sku_param:
            # Filter products based on the provided 'sku' parameter
            products = Product.objects.filter(sku=sku_param)
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            # Handle the case when 'sku' parameter is not provided.
            # For example, return all products.
            products = Product.objects.all()
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

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