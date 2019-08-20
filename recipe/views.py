"""
Recipe API Views
"""
from rest_framework import generics
from rest_framework.response import Response
from recipe.permissions import IsOwnerOrReadOnly
from .models import Recipe, Ingredients
from .serializers import RecipeSerializer, IngredientsSerializer


class RecipeList(generics.ListCreateAPIView):
    """
    Recipe listing view
    """
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    def get_queryset(self):
        queryset = Recipe.objects.all()
        user = self.request.query_params.get('user_id')

        if user:
            queryset = queryset.filter(user_id=user)

        return queryset

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return self.create(request, *args, **kwargs)

        return Response(status=403, data={
            'user': request.user.id,
            "error": "not authorized to add"
        })


class RecipeListFollowing(generics.ListAPIView):
    serializer_class = RecipeSerializer

    def get_queryset(self):
        """
        To filter recipes by followers
        :return:
        """
        id_arr = []
        users_profiles = self.request.user.userprofile.follows.all()
        for users_profile in users_profiles:
            id_arr.append(users_profile.user.id)
        return Recipe.objects.filter(user_id__in=id_arr)


class RecipeDetail(generics.RetrieveUpdateDestroyAPIView):  # pylint:disable=too-many-ancestors
    """
    CBV for Recipe detail page
    """
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (IsOwnerOrReadOnly,)


class IngredientList(generics.ListCreateAPIView):
    """
    CBV for IngredientList
    """
    queryset = Ingredients.objects.all()
    serializer_class = IngredientsSerializer
