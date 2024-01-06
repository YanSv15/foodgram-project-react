import base64

from django.shortcuts import get_object_or_404
from django.core.files.base import ContentFile
from rest_framework import serializers, status
from rest_framework.response import Response

from posts.models import Ingredient, IngredientsRecipe


def create_ingredients(ingredients, recipe):
    """Вспомогательная функция для добавления ингредиентов.
    Используется при создании/редактировании рецепта."""
    ingredient_list = []
    for ingredient in ingredients:
        current_ingredient = get_object_or_404(Ingredient,
                                               id=ingredient.get('id'))
        amount = ingredient.get('amount')
        ingredient_list.append(
            IngredientsRecipe(
                recipe=recipe,
                ingredient=current_ingredient,
                amount=amount
            )
        )
    IngredientsRecipe.objects.bulk_create(ingredient_list)
