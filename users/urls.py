from django.conf.urls import url

from . import views
from rest_framework.authtoken import views as auth_view

urlpatterns = [
    url('create/', views.UserCreate.as_view(), name='user-create'),
    url('login/', views.CustomAuthToken.as_view(), name='user-login')

]
