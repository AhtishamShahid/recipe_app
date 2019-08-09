from rest_framework import generics, permissions
from rest_framework.response import Response

from .models import Recipe, Ingredients
from .serializers import RecipeSerializer, IngredientsSerializer


class RecipeList(generics.ListCreateAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    # permission_classes = [permissions.IsAuthenticated]
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return self.create(request, *args, **kwargs)

        return Response(status=403, data={
            'user': request.user.id,
            "error": "not authorized to add"
        })


class RecipeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer


class IngredientList(generics.ListCreateAPIView):
    queryset = Ingredients.objects.all()
    serializer_class = IngredientsSerializer
