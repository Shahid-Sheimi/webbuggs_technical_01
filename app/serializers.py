from rest_framework import serializers
from .models import ProductCategory, SubCategory, Color, Product,CustomUser

class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = '__all__'
class ProductSerializer(serializers.ModelSerializer):
    category = ProductCategorySerializer()

    class Meta:
        model = Product
        fields = ['title', 'description', 'sku', 'category']
class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['name', 'short_name','description', 'created_by']
class ProductSerializer(serializers.ModelSerializer):
    category = ProductCategorySerializer()  # Assuming you have a ProductCategorySerializer
    class Meta:
        model = Product
        fields = ['title', 'description', 'sku', 'category']
    def create(self, validated_data):
        # Extract the nested data for the category
        category_data = validated_data.pop('category', None)
        # Retrieve the user from the request
        user = self.context['request'].user
        # Ensure that the user is a CustomUser instance
        if not isinstance(user, CustomUser):
            raise ValueError("Invalid user type. Must be a CustomUser instance.")
        # Create the product without the nested category and set the created_by field
        product = Product.objects.create(created_by=user, **validated_data)
        # If category_data is provided, set the category for the created product
        if category_data:
            product.category = SubCategory.objects.create(**category_data, created_by=user)
            product.save()
        return product

class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = '__all__'

class ProductFilterSerializer(serializers.Serializer):
    keyword = serializers.CharField(required=False, allow_blank=True)
    sku = serializers.CharField(required=False, allow_blank=True)

class UserProductInfoSerializer(serializers.ModelSerializer):
    product_count = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'product_count']

    def get_product_count(self, obj):
        return obj.product_count