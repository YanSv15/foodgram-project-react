from rest_framework.routers import DefaultRouter

from django.urls import include, path

from api.views import TagsViewSet, IngredientsViewSet, RecipeViewSet
from users.views import UserViewSet, FollowViewSet


router = DefaultRouter()
router.register('tags', TagsViewSet, basename='tags')
router.register('ingredient', IngredientsViewSet, basename='ingredient')
router.register('recipe', RecipeViewSet, basename='recipe')
router.register('users', UserViewSet, basename='users')


urlpatterns = [
    path('', include(router.urls)),
    # path('', include('djoser.urls')),
    # path('auth/', include('djoser.urls.authtoken'))
]
