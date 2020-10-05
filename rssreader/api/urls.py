from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from api import views

urlpatterns = [
    path('users/register', views.UserCreate.as_view(), name='user_register'),
    path('users/login', obtain_auth_token, name='user_login'),
    path('test', views.TestView.as_view(), name='test'),
]
