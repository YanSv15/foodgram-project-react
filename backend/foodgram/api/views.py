
from rest_framework import viewsets, filters
# from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import SAFE_METHODS
from rest_framework.views import APIView

from posts.models import Tag, Ingredient, Recipe
from api import serializers
from api.permission import AdminOrReadOnly, AuthorOrReadOnly
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend


class TagsViewSet(viewsets.ModelViewSet):
    # permission_classes = (AdminOrReadOnly,)
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer
    pagination_class = None
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = ('name', 'slug')
    search_fields = ('^name',)


class IngredientsViewSet(viewsets.ModelViewSet):
    # permission_classes = (AdminOrReadOnly,)
    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter, )
    # filterset_fields = ('name')
    search_fields = ('^name',)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    # serializer_class = serializers.RecipeReadSerializer
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = ('author', 'ingredients', 'name', 'cooking_time')
    # permission_classes = (AuthorOrReadOnly)
    search_fields = ('^name', )

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return serializers.RecipeReadSerializer
        return serializers.RecipeWriteSerializer


class FollowViewSet(viewsets.ModelViewSet):
    pass


class ShoppingCardViewSet(viewsets.ModelViewSet):
    pass


class FavoriteRecipeViewSet(viewsets.ModelViewSet):
    pass
