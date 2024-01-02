from rest_framework import serializers
from .models import CustomUser
from rest_framework.generics import CreateAPIView

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'
class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

class UserSignupView(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer  # Set the serializer class

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'
