"""
# Create your tests here.
"""
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate
from rest_framework import status
from recipe.views import RecipeList, RecipeListFollowing
from users.views import FollowUser
from .models import Recipe, Ingredients


def create_recipe(data, user):
    """
    # Make an authenticated request to the view...
    :param data:
    :param user:
    :return:
    """
    factory = APIRequestFactory()
    view = RecipeList.as_view()

    request = factory.post(reverse('recipes'), data=data)
    force_authenticate(request, user=user)
    response = view(request)
    return response


class RecipeTest(APITestCase):
    """
    Test Recipe CRUD
    """

    def setUp(self):
        """
         # We want to go ahead and originally create a RecipeTest.
        :return:
        """
        self.test_user = User.objects.create_user('testuser', 'test@example.com', 'testpassword')
        self.ingredient = Ingredients.objects.create(title='Meat')
        self.recipe = Recipe(title='Chicken', description='This is recipe'
                             , directions='make it', user_id=self.test_user.pk).save()

        self.create_url = reverse('recipes')
        self.token = Token.objects.create(user=self.test_user)

    def test_create_recipe(self):
        """
        Ensure we can create a new recipe and .
        """
        data = {
            'title': 'title',
            'description': 'title',
            'directions': 'title',
            'ingredients': [
                1
            ]
        }
        response = create_recipe(data, self.test_user)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], data['title'])
        self.assertEqual(response.data['description'], data['description'])
        self.assertEqual(response.data['directions'], data['directions'])
        self.assertEqual(response.data['user_id'], self.test_user.id)
        self.assertEqual(response.data['ingredients'], data['ingredients'])
        self.assertEqual(Recipe.objects.count(), 2)

    def test_create_recipe_without_title(self):
        """
        Ensure we can create a new recipe and .
        """
        data = {
            'description': 'title',
            'directions': 'title',
        }

        response = create_recipe(data, self.test_user)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Recipe.objects.count(), 1)
        self.assertEqual(len(response.data['title']), 1)

    def test_create_recipe_without_description(self):
        """
        Ensure we can create a new recipe and .
        """
        data = {
            'title': 'title',
            'directions': 'title',
        }
        response = create_recipe(data, self.test_user)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Recipe.objects.count(), 1)
        self.assertEqual(len(response.data['description']), 1)

    def test_create_recipe_without_directions(self):
        """
        Ensure we can create a new recipe and .
        """
        data = {
            'title': 'title',
            'description': 'title',
        }

        response = create_recipe(data, self.test_user)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Recipe.objects.count(), 1)
        self.assertEqual(len(response.data['directions']), 1)

    def test_create_recipe_without_auth(self):
        """
        Ensure we can create a new recipe and .
        """
        data = {
            'title': 'title',
            'description': 'title',
            'directions': 'title',
        }

        response = self.client.post(reverse('recipes'), data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Recipe.objects.count(), 1)

    def test_recipe_list_page(self):
        """
        test_recipe_list_page
        :return:
        """
        response = self.client.get(reverse('recipes'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_recipe_detail_page(self):
        """
        test_recipe_detail_page
        :return:
        """
        recipe = Recipe.objects.first()
        response = self.client.get(reverse('recipes') + str(recipe.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def user_cannot_edit_others_recipe(self):
        """
        user_cannot_edit_others_recipe
        :return:
        """

    def user_cannot_delete_others_recipe(self):
        """
        user_cannot_delete_others_recipe
        :return:
        """

    def add_ingredients_to_recipe(self):
        """
        add_ingredients_to_recipe
        :return:
        """

    def test_following_recipe_list_page(self):
        """
        test_recipe_list_page
        :return:
        """
        user = User.objects.create_user('testuser2', 'test2@example.com', 'testpassword')
        i = Ingredients.objects.create(title='Meat')
        data = {
            'title': 'title',
            'description': 'title',
            'directions': 'title',
            'ingredients': [
                i.id
            ]
        }
        create_recipe(data, user)
        """
        Created follower
        """

        factory = APIRequestFactory()
        view = FollowUser.as_view()
        request = factory.post(reverse('follow-user'), data={'user_id': user.pk})
        force_authenticate(request, user=self.test_user)
        view(request)

        factory = APIRequestFactory()
        view = RecipeListFollowing.as_view()
        request = factory.get(reverse('recipes-followings'))
        force_authenticate(request, user=self.test_user)
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
