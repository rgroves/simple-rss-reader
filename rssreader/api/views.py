from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import AllowAny
from api.serializers import UserSerializer

# Define the view to be used with  the user creation (registration) endpoint.
class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny)
