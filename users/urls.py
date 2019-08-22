"""
user Application urls
"""
from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    # url('create/', views.UserCreate.as_view(), name='user-create'),
    url('login/', views.CustomAuthToken.as_view(), name='user-login'),
    path('users/', views.UserList.as_view(), name='user-create'),
    path('users/change-password/', views.APIChangePasswordView.as_view(),
         name='user-change-password'),
    path('users/follow-request/', views.FollowUser.as_view(), name='follow-user'),
    path('users/<int:pk>/', views.UserDetail.as_view()),

]
