from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from .serializers import UserLoginSerializer, UserSerializer
CustomUser = get_user_model()

class UserSignupView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = []
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        # Send welcome email
        user_email = serializer.validated_data['email']
        welcome_subject = 'Welcome to My App'
        welcome_message = f'Thank you for signing up on My App, {user_email}!'
        send_mail(welcome_subject, welcome_message, settings.DEFAULT_FROM_EMAIL, [user_email])
        headers = self.get_success_headers(serializer.data)
        return Response({'message': 'User created successfully. Check your email for the welcome message.'},
                        status=status.HTTP_201_CREATED, headers=headers)
class UserLoginView(generics.CreateAPIView):
    serializer_class = UserLoginSerializer
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        user = CustomUser.objects.filter(email=email).first()
        if user and user.check_password(password):
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        return Response({'non_field_errors': ['Invalid credentials', 'Please check your email and password.']}, status=status.HTTP_401_UNAUTHORIZED)
class UserListView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    # permission_classes = [permissions.IsAuthenticated]
class UserDetailView(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class UserUpdateView(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class UserDeleteView(generics.DestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
