"""
Create your tests here.
"""
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate
from rest_framework import status
from users.views import APIChangePasswordView, follow_user


class UserTest(APITestCase):
    """
    User Module test cases.
    """

    def setUp(self):
        """
        We want to go ahead and originally create a user
        """
        self.test_user = User.objects.create_user('testuser', 'test@example.com', 'testpassword')

        # URL for creating an account.
        self.create_url = reverse('user-create')

    def test_create_user(self):
        """
        Ensure we can create a new user and a valid token is created with it.
        """
        data = {
            'username': 'zombie',
            'email': 'zombie@gmail.com',
            'password': 'zombie123'
        }

        response = self.client.post(self.create_url, data, format='json')
        user = User.objects.latest('id')

        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], data['username'])
        self.assertEqual(response.data['email'], data['email'])
        self.assertFalse('password' in response.data)
        Token.objects.get(user=user)
        # self.assertEqual(response.data['token'], token.key)

    def test_create_user_with_short_password(self):
        """
        Ensure user is not created for password lengths less than 8.
        """
        data = {
            'username': 'ahtisham',
            'email': 'ahtisham@example.com',
            'password': '123'
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['password']), 1)

    def test_create_user_with_no_password(self):
        """
        Ensure user test_create_user_with_no_password
        """
        data = {
            'username': 'shahid',
            'email': 'shahid@gmail.com',
            'password': ''
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['password']), 1)

    def test_create_user_with_too_long_username(self):
        """
        Ensure user test_create_user_with_too_long_username
        """
        data = {
            'username': 'ahtisham' * 30,
            'email': 'ahtisham@example.com',
            'password': '123456'
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['username']), 1)

    def test_create_user_with_no_username(self):
        """
        test_create_user_with_no_username
        """
        data = {
            'username': '',
            'email': 'foobarbaz@example.com',
            'password': 'foobar'
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['username']), 1)

    def test_create_user_with_preexisting_username(self):
        """
        test_create_user_with_preexisting_username
        """
        data = {
            'username': 'testuser',
            'email': 'user@example.com',
            'password': 'testuser'
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['username']), 1)

    def test_create_user_with_preexisting_email(self):
        """
        test_create_user_with_preexisting_email
        """
        data = {
            'username': 'testuser2',
            'email': 'test@example.com',
            'password': 'testuser'
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['email']), 1)

    def test_create_user_with_invalid_email(self):
        """
        test_create_user_with_invalid_email
        """
        data = {
            'username': 'foobarbaz',
            'email': 'testing',
            'passsword': 'foobarbaz'
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['email']), 1)

    def test_create_user_with_no_email(self):
        """
        test_create_user_with_no_email
        """
        data = {
            'username': 'foobar',
            'email': '',
            'password': 'foobarbaz'
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['email']), 1)

    def test_has_correct_recipe_count(self):
        """
        test_has_correct_recipe_count
        """

    def test_has_correct_recipe_list(self):
        """
        test_has_correct_recipe_list
        """


class LoginTest(APITestCase):
    """
    Login mechanism test
    """

    def setUp(self):
        """
        Setup users for testing
        """
        # URL for creating an account.
        self.create_url = reverse('user-login')

    def test_create_user(self):
        """
        Ensure we can create a new user and user can login
        """
        data = {
            'username': 'zombie',
            'email': 'zombie@gmail.com',
            'password': 'zombie123'
        }

        self.client.post(reverse('user-create'), data, format='json')
        user = User.objects.latest('id')
        response = self.client.post(reverse('user-login'), data, format='json')
        token = Token.objects.get(user=user)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user_id'], user.id)
        self.assertEqual(response.data['username'], data['username'])
        self.assertEqual(response.data['email'], data['email'])
        self.assertEqual(response.data['token'], token.key)


def make_change_pwd_request(change_password_data, user):
    """
    To make authenticated Api request to change passowrd
    :param change_password_data:
    :param user:
    :return:
    """
    factory = APIRequestFactory()
    view = APIChangePasswordView.as_view()
    request = factory.put(reverse('user-change-password'), data=change_password_data)
    force_authenticate(request, user=user)
    return view(request)


class ChangePasswordTest(APITestCase):
    """
    Tests for change password Api
    """

    def setUp(self):
        """
        testing basic needed urls and data
        :return:
        """
        # URL for creating an account.
        self.change_password = reverse('user-change-password')

        # create user for testing
        self.user_data = {
            'username': 'zombie',
            'email': 'zombie@gmail.com',
            'password': 'zombie123'
        }

        self.client.post(reverse('user-create'), self.user_data, format='json')
        self.user = User.objects.latest('id')

    def test_change_user_change_password(self):
        """
        Ensure we can create a new user and test change password process
        """

        # Make an authenticated request to the view...
        change_password_data = {
            'old_password': 'zombie123',
            'confirmed_password': '123465789',
            'password': '123465789'
        }
        response = make_change_pwd_request(change_password_data, self.user)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_change_password_missing_old(self):
        """
        Test with missing old password
        """

        # Make an authenticated request to the view...
        change_password_data = {
            'confirmed_password': '123465789',
            'password': '123465789'
        }
        response = make_change_pwd_request(change_password_data, self.user)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(response.data['old_password']), 1)

    def test_user_change_password_missing_confirm(self):
        """
        Test with missing confirm password
        """

        # Make an authenticated request to the view...
        change_password_data = {
            'old_password': 'zombie123',
            'password': '123465789'
        }
        response = make_change_pwd_request(change_password_data, self.user)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(response.data['confirmed_password']), 1)

    def test_user_change_password_missing_password(self):
        """
        Test with missing password
        """
        # Make an authenticated request to the view...
        change_password_data = {
            'old_password': 'zombie123',
            'confirmed_password': '123465789',
        }
        response = make_change_pwd_request(change_password_data, self.user)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(response.data['password']), 1)

    def test_user_change_password_without_auth(self):
        """
        Test with change password without auth
        """
        # Make an authenticated request to the view...
        change_password_data = {
            'old_password': 'zombie123',
            'confirmed_password': '123465789',
            'password': '123465789'
        }
        response = self.client.put(reverse('user-change-password'), data=change_password_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class FollowersManagementTests(APITestCase):
    """
    Test user follower mechanism is working
    """

    def setUp(self):
        """
        Add 2 users for testing
        """
        self.usr1, created = User.objects.get_or_create(username='tim')
        self.usr2, created = User.objects.get_or_create(username='chris')
        if created:
            print(True)
        self.url = reverse('follow-user')

    def test_follow_status(self):
        """
        Test user follower mechanism is working
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        factory = APIRequestFactory()
        view = follow_user
        request = factory.post(self.url, data={'user_id': self.usr2.pk})
        force_authenticate(request, user=self.usr1)
        auth_response = view(request)
        self.assertEqual(auth_response.status_code, status.HTTP_200_OK)
