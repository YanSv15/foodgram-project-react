from rest_framework.routers import DefaultRouter

from django.urls import include, path

from api.views import (TagsViewSet, IngredientsViewSet,
                       RecipeViewSet, FavoriteViewSet,
                       ShoppingCartViewSet,
                       SubcribeCreateDeleteViewSet)
from users.views import UserViewSet


router = DefaultRouter()

router.register('recipe', RecipeViewSet, basename='recipe')
router.register('ingredient', IngredientsViewSet, basename='ingredient')
router.register('tags', TagsViewSet, basename='tags')
router.register(
    r'recipe/(?P<recipe_id>\d+)/favorite', FavoriteViewSet,
    basename='favorite')
router.register(
    r'recipe/(?P<recipe_id>\d+)/shopping_cart', ShoppingCartViewSet,
    basename='shoppingcart')
router.register('users', UserViewSet, basename='users')

router.register('recipe/(?P<user_id>\d+)/recipe',
                SubcribeCreateDeleteViewSet, basename='recipe-create')


urlpatterns = [
    path('', include(router.urls)),
]
