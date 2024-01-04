from rest_framework.routers import DefaultRouter

from django.urls import include, path

from api.views import (TagsViewSet, IngredientsViewSet,
                       RecipeViewSet, FavoriteViewSet,
                       ShoppingCartViewSet,
                       SubcribeCreateDeleteViewSet)
from users.views import UserViewSet


router = DefaultRouter()

router.register('users', UserViewSet, basename='users')
router.register('recipes', RecipeViewSet, basename='recipes')
router.register('ingredients', IngredientsViewSet, basename='ingredients')
router.register('tags', TagsViewSet, basename='tags')
router.register(
    r'recipes/(?P<recipe_id>\d+)/favorite', FavoriteViewSet,
    basename='favorite')
router.register(
    r'recipes/(?P<recipe_id>\d+)/shopping_cart', ShoppingCartViewSet,
    basename='shoppingcart')


router.register(r'users/(?P<user_id>\d+)/subscribe',
                SubcribeCreateDeleteViewSet, basename='subscribe')


urlpatterns = [
    path('', include(router.urls)),
]
