# Create your views here.
"""
user Application views
"""
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import generics
from django.contrib.auth.models import User
from .serializers import UserSerializer, UserPasswordChangeSerializer, UserProfileSerializer


class CustomAuthToken(ObtainAuthToken):
    """
    login procedure
    """

    def post(self, request, *args, **kwargs):
        """
        authenticate user and returns Auth Token
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)  # pylint: disable=unused-variable
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email,
            'username': user.username
        })


class UserList(generics.ListCreateAPIView):
    """
    User list view
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        queryset = User.objects.all()
        user = self.request.query_params.get('my_followings')

        following_ids = []
        if user:
            followings = User.objects.get(pk=self.request.user.pk).userprofile.follows.all()
            for follow in followings:
                following_ids.append(follow.user_id)
            queryset = User.objects.filter(id__in=following_ids).all()
        return queryset


class UserDetail(generics.RetrieveAPIView):
    """
    user detail view
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class APIChangePasswordView(generics.UpdateAPIView):
    """
    change password api view
    """
    serializer_class = UserPasswordChangeSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        """
        custom response
        :return:
        """
        return self.request.user


class FollowUser(generics.CreateAPIView):
    """
    Follow user crud added
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = UserProfileSerializer
