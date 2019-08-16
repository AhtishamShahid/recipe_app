# Create your tests here.
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate
from django.contrib.auth.models import User
from rest_framework import status

from users.views import APIChangePasswordView


class UserTest(APITestCase):
    def setUp(self):
        # We want to go ahead and originally create a user.
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
        token = Token.objects.get(user=user)
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
        pass

    def test_has_correct_recipe_list(self):
        pass


class LoginTest(APITestCase):
    def setUp(self):
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
    factory = APIRequestFactory()
    view = APIChangePasswordView.as_view()
    request = factory.put(reverse('user-change-password'), data=change_password_data)
    force_authenticate(request, user=user)
    return view(request)


class ChangePasswordTest(APITestCase):
    def setUp(self):
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
    def setUp(self):
        tim, c = User.objects.get_or_create(username='tim')
        chris, c = User.objects.get_or_create(username='chris')
        print(tim, chris)
        tim.userprofile.follows.add(chris.userprofile)  # chris follows tim
        self.b = tim.userprofile.follows.all()  # list of userprofiles of users that tim follows
        self.a = chris.userprofile.followed_by.all()  # list of userprofiles of users that follow chris

    def test_follow_status(self):
        print(self.a[0])
        print(self.b[0])
