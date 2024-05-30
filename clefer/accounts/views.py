from rest_framework import viewsets, permissions, generics
from django.contrib import auth
from .serializers import UserSerializer

class UserList(generics.ListAPIView):
    queryset = auth.models.User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class UserDetail(generics.RetrieveAPIView):
    queryset = auth.models.User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class UserCreate(generics.CreateAPIView):
    queryset = auth.models.User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
