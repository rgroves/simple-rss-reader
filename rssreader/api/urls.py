from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from api import views

urlpatterns = [
    path('users/register', views.UserCreate.as_view(), name='user_register'),
    path('users/login', views.UserLogin.as_view(), name='user_login'),
    path('test', views.TestView.as_view(), name='test'),
    path('feeds/add', views.FeedCreate.as_view(), name='feeds_add'),
]
