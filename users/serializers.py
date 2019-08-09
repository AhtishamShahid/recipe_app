from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User

from recipe.models import Recipe


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all())],
        max_length=32,
    )
    password = serializers.CharField(min_length=8, write_only=True)
    recipe_count = serializers.SerializerMethodField('get_recipe_count')
    recipe = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    def get_recipe_count(self, obj):
        return Recipe.objects.filter(user_id=obj.pk).count()

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'],
                                        validated_data['password'])
        Token.objects.get_or_create(user=user)
        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'recipe_count', 'recipe')
