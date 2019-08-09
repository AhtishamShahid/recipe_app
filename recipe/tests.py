from django.test import TestCase

from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate
from django.contrib.auth.models import User
from rest_framework import status
from recipe.views import RecipeList
from .models import Recipe, Ingredients


# from rest_framework.reverse import reverse

def create_recipe(data, user):
    factory = APIRequestFactory()
    view = RecipeList.as_view()

    # Make an authenticated request to the view...
    request = factory.post(reverse('recipes'), data=data)
    force_authenticate(request, user=user)
    response = view(request)
    return response


class RecipeTest(APITestCase):
    def setUp(self):
        # We want to go ahead and originally create a RecipeTest.
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
        }
        response = create_recipe(data, self.test_user)
        self.assertEqual(Recipe.objects.count(), 2)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], data['title'])
        self.assertEqual(response.data['description'], data['description'])
        self.assertEqual(response.data['directions'], data['directions'])
        self.assertEqual(response.data['user_id'], self.test_user.id)

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

    def test_create_recipe_without_Auth(self):
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

    def user_cannot_edit_others_recipe(self):
        pass

    def user_cannot_delete_others_recipe(self):
        pass

    def add_ingredients_to_recipe(self):
        pass
