from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from api.serializers import UserSerializer

from rest_framework.views import APIView
from rest_framework.response import Response

# Define the view to be used with the user creation (registration) endpoint.
class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        """
        Override create to be able to return access_token registration call.
        """
        # Serialize incoming data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Create user, get user's token and send response.
        self.perform_create(serializer)
        token = Token.objects.create(user=serializer.instance)
        return Response({'access_token': token.key}, status=status.HTTP_201_CREATED)

class UserLogin(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        """
        Override create to be able to return user id during login call.
        """
        # Serialize incoming data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        # Get user's token and send response.
        token = Token.objects.get(user=user)
        return Response({'access_token': token.key, 'user_id': user.id}, status=status.HTTP_200_OK)

class TestView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Just a test.'}
        return Response(content)
