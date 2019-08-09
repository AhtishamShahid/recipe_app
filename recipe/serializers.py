from rest_framework import serializers
from rest_framework.fields import *
from rest_framework.relations import PrimaryKeyRelatedField
from .models import Recipe, Ingredients


class IngredientsSerializer(PrimaryKeyRelatedField, serializers.ModelSerializer):
    class Meta:
        model = Ingredients
        fields = '__all__'


class RecipeSerializer(serializers.ModelSerializer):
    id = IntegerField(label='ID', read_only=True)
    title = CharField(max_length=100, required=True)
    description = CharField(max_length=600, required=True)
    directions = CharField(max_length=600, required=True)
    user_id = PrimaryKeyRelatedField(read_only=True)
    pub_date = DateTimeField(read_only=True)
    ingredients_set = IngredientsSerializer(read_only=True, many=True)

    def create(self, validated_data):
        return Recipe.objects.create(**validated_data, user_id=self.context['request'].user.id)

    class Meta:
        model = Recipe
        fields = ['id', 'title', 'description', 'directions', 'user_id', 'pub_date', 'ingredients_set']
