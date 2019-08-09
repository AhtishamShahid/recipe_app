from rest_framework import serializers
from rest_framework.fields import *
from rest_framework.relations import PrimaryKeyRelatedField
from .models import Recipe, Ingredients


class IngredientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredients
        fields = '__all__'
        depth = 1


class RecipeSerializer(serializers.ModelSerializer):
    id = IntegerField(label='ID', read_only=True)
    title = CharField(max_length=100, required=True)
    description = CharField(max_length=600, required=True)
    directions = CharField(max_length=600, required=True)
    user_id = PrimaryKeyRelatedField(read_only=True)

    def create(self, validated_data):
        return Recipe.objects.create(**validated_data, user_id=self.context['request'].user.id)

    class Meta:
        model = Recipe
        fields = ['id', 'title', 'description', 'directions', 'user_id']
        # ingredients = serializers.PrimaryKeyRelatedField(many=True, queryset=Ingredients.objects.all())
