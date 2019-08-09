from django.conf.urls import url
from django.urls import path

from . import views
from rest_framework.authtoken import views as auth_view

urlpatterns = [
    # url('create/', views.UserCreate.as_view(), name='user-create'),
    url('login/', views.CustomAuthToken.as_view(), name='user-login'),
    path('users/', views.UserList.as_view(), name='user-create'),
    path('users/<int:pk>/', views.UserDetail.as_view()),
]
