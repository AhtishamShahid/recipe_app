from django.shortcuts import render

# Create your views here.
from rest_framework import generics

# Create your views here.
from .models import Recipe, Ingredients
from .serializers import RecipeSerializer, IngredientsSerializer


class RecipeList(generics.ListCreateAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer


class IngredientList(generics.ListCreateAPIView):
    queryset = Ingredients.objects.all()
    serializer_class = IngredientsSerializer
