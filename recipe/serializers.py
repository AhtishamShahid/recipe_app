from rest_framework import serializers
from .models import Recipe, Ingredients


class IngredientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredients
        fields = '__all__'
        depth = 1


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = '__all__'
        ingredients = serializers.PrimaryKeyRelatedField(many=True, queryset=Ingredients.objects.all())
