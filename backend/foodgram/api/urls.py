from rest_framework.routers import DefaultRouter
from djoser import views as djoser_views

from django.urls import include, path

from api.views import (TagsViewSet, IngredientsViewSet,
                       RecipeViewSet, FavoriteViewSet, ShoppingCartViewSet, SubcribeCreateDeleteViewSet, SubscribeViewSet,RegisterView)
from users.views import UserViewSet


router = DefaultRouter()

router.register('recipe', RecipeViewSet, basename='recipe')
router.register('ingredient', IngredientsViewSet, basename='ingredient')
router.register('tags', TagsViewSet, basename='tags')
router.register(
    r'users/(?P<user_id>\d+)/subscribe', SubscribeViewSet,
    basename='subscribe')
router.register(
    r'recipe/(?P<recipe_id>\d+)/favorite', FavoriteViewSet,
    basename='favorite')
router.register(
    r'recipe/(?P<recipe_id>\d+)/shopping_cart', ShoppingCartViewSet,
    basename='shoppingcart')
router.register('users', UserViewSet, basename='users')

router.register('recipe/(?P<user_id>\d+)/recipe', SubcribeCreateDeleteViewSet, basename='recipe-create')

# urlpatterns_favorite = [
    # path('recipe/favorite/<int:pk>/', FavoriteCreateView.as_view(), name='favorite'),
    # path('recipe/favorite/<int:pk>/', FavoriteDeleteView.as_view(), name='favorite')
# ]


urlpatterns = [
    path('', include(router.urls)),
    # path('register/', djoser_views.UserCreateView.as_view(), name='user-create'),
    # path('', include(urlpatterns_favorite))
    # path('', include('djoser.urls')),
    # path('auth/', include('djoser.urls.authtoken'))
]
