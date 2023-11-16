from django.contrib import admin

from .models import (Ingredient, Recipe, Tag,
                     IngredientsRecipe, Favorite, ShoppingCard, Follow)


admin.site.register(Tag)
admin.site.register(Ingredient)
admin.site.register(Recipe)
admin.site.register(Favorite)
admin.site.register(IngredientsRecipe)
admin.site.register(ShoppingCard)
admin.site.register(Follow)