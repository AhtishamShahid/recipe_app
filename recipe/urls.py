# from django.conf.urls import urlrec
from django.urls import path

from . import views
from rest_framework.authtoken import views as auth_view

urlpatterns = [
    path('recipes/', views.RecipeList.as_view(), name='recipes'),
    path('recipes/<int:pk>', views.RecipeDetail.as_view(), name='recipes-detail'),
    path('ingredients/', views.IngredientList.as_view()),
]
