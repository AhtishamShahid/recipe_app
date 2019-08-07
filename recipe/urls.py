from django.conf.urls import url

from . import views
from rest_framework.authtoken import views as auth_view

urlpatterns = [
    url('recipes/', views.RecipeList.as_view()),
]
