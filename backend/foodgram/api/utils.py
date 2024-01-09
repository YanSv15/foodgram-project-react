from posts.models import IngredientsRecipe


def create_ingredients(ingredients, recipe):
    """Вспомогательная функция для добавления ингредиентов.
    Используется при создании/редактировании рецепта."""
    ingredient_list = []
    for ingredient in ingredients:
        ingredient_id = ingredient.get('id')
        amount = ingredient.get('amount')
        ingredient_list.append(
            IngredientsRecipe(
                recipe=recipe,
                ingredient_id=ingredient_id,
                amount=amount
            )
        )
    IngredientsRecipe.objects.bulk_create(ingredient_list)
