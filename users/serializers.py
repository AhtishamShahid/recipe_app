from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User

from recipe.models import Recipe
from users.models import UserProfile


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
    following = serializers.SerializerMethodField('get_if_following')

    def get_recipe_count(self, obj):
        return Recipe.objects.filter(user_id=obj.pk).count()

    def get_if_following(self, obj):
        is_follower = obj.userprofile.followed_by.filter(user_id=self.context['request'].user.id)
        print(is_follower)
        if is_follower:
            return True
        else:
            return False

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'],
                                        validated_data['password'])
        Token.objects.get_or_create(user=user)
        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'recipe_count', 'recipe', 'following')


class UserPasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, max_length=30)
    password = serializers.CharField(required=True, max_length=30)
    confirmed_password = serializers.CharField(required=True, max_length=30)

    def validate(self, data):
        # add here additional check for password strength if needed
        if not self.context['request'].user.check_password(data.get('old_password')):
            raise serializers.ValidationError({'old_password': 'Wrong password.'})

        if data.get('confirmed_password') != data.get('password'):
            raise serializers.ValidationError({'password': 'Password must be confirmed correctly.'})

        return data

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()
        return instance

    def create(self, validated_data):
        pass

    @property
    def data(self):
        return {'Success': True}
