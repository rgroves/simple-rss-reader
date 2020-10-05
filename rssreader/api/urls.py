from django.urls import path
from api import views

urlpatterns = [
    path('users/register', views.UserCreate.as_view())
]
