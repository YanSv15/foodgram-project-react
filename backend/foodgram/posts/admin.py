from django.contrib import admin

from .models import (Ingredient, Recipe, Tag,
                     IngredientsRecipe, Favorite, ShoppingCard, Subscribe)


admin.site.register(Tag)
admin.site.register(Ingredient)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'name', 'image', 'text',)


admin.site.register(Favorite)
admin.site.register(IngredientsRecipe)
admin.site.register(ShoppingCard)
admin.site.register(Subscribe)
