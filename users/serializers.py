"""
user Module serializer
"""
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User
from recipe.models import Recipe


class UserSerializer(serializers.ModelSerializer):
    """
    user model serializer
    """
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

    def get_recipe_count(self, obj):  # pylint: disable=no-self-use
        """
        adds count of recipe in response
        :param obj:
        :return:
        """
        return Recipe.objects.filter(user_id=obj.pk).count()

    def get_if_following(self, obj):
        """
        adds if auth user is following listed user
        :param obj:
        :return:
        """

        return obj.userprofile.followed_by.filter(user_id=self.context['request'].user.id).exists()

    def create(self, validated_data):
        """
        over rides default create to add user id in DB
        :param validated_data:
        :return:
        """
        user = User.objects.create_user(validated_data['username'], validated_data['email'],
                                        validated_data['password'])
        Token.objects.get_or_create(user=user)
        return user

    class Meta:
        """
        serializer meta data
        """
        model = User
        fields = ('id', 'username', 'email', 'password', 'recipe_count', 'recipe', 'following')


class UserPasswordChangeSerializer(serializers.Serializer):
    """
    format and validated Password change API request
    """
    old_password = serializers.CharField(required=True, max_length=30)
    password = serializers.CharField(required=True, max_length=30)
    confirmed_password = serializers.CharField(required=True, max_length=30)

    def validate(self, attrs):
        """
         add here additional check for password strength if needed
        """
        if not self.context['request'].user.check_password(attrs.get('old_password')):
            raise serializers.ValidationError({'old_password': 'Wrong password.'})

        if attrs.get('confirmed_password') != attrs.get('password'):
            raise serializers.ValidationError({'password': 'Password must be confirmed correctly.'})

        return attrs

    def update(self, instance, validated_data):
        """
        password update
        :param instance:
        :param validated_data:
        :return:
        """
        instance.set_password(validated_data['password'])
        instance.save()
        return instance

    def create(self, validated_data):
        """abstract class method"""

    @property
    def data(self):
        return {'Success': True}
