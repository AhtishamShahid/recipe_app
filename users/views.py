# Create your views here.
"""
user Application views
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import generics
from django.contrib.auth.models import User
from .serializers import UserSerializer, UserPasswordChangeSerializer


class UserCreate(APIView):
    """
    Creates the user.
    """

    def post(self, request):
        """
        over ride post method to make custom token for auth
        :param request:
        :param format:
        :return:
        """
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                token = Token.objects.create(user=user)
                json = serializer.data
                json['token'] = token.key
                return Response(json, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
        token, created = Token.objects.get_or_create(user=user) # pylint: disable=unused-variable
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
    paginate = 3


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


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def follow_user(request):
    """
    User can follow another user
    :param request:
    :return:
    """
    if 'user_id' in request.POST:
        try:
            to_follow = User.objects.get(pk=request.POST['user_id'])
            follower = User.objects.get(pk=request.user.pk)
            follower.userprofile.follows.add(to_follow.userprofile)
            return Response(status=status.HTTP_200_OK, data={'Success': True})
        except User.DoesNotExist:
            Response(status=status.HTTP_404_NOT_FOUND)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
