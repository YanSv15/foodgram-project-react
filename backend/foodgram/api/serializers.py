from django.db import transaction
from django.core.files.base import ContentFile
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from djoser.serializers import (UserCreateSerializer
                                as DjoserUserCreateSerializer)

from posts.models import (Tag, Ingredient, Recipe, IngredientsRecipe,
                          Favorite, ShoppingCard, Subscribe)
from .utils import create_ingredients

User = get_user_model()


class UserCreateSerializer(DjoserUserCreateSerializer):
    class Meta(DjoserUserCreateSerializer.Meta):
        model = User
        fields = ('id', 'email', 'username', 'password',
                  'first_name', 'last_name',)


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed')

    def get_is_subscribed(self, obj):
        return (self.context.get('request').user.is_authenticated
                and Subscribe.objects.filter(
                    user=self.context.get('request').user,
                    author=obj
        ).exists())


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = fields = '__all__'


class IngredientWriteSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    amount = serializers.IntegerField()

    class Meta:
        model = Ingredient
        fields = ['id', 'amount']


class IngredientRecipeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    measurement_unit = serializers.CharField()
    name = serializers.CharField()

    class Meta:
        model = IngredientsRecipe
        fields = ('id', 'name', 'measurement_unit')


class RecipeReadSerializer(serializers.ModelSerializer):
    author = UserSerializer(
        read_only=True,
    )
    ingredients = IngredientRecipeSerializer(
        read_only=True,
        many=True
    )
    tags = TagSerializer(
        read_only=True,
        many=True,
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        fields = ('id', 'author', 'ingredients', 'tags', 'image',
                  'name', 'text', 'cooking_time', 'is_favorited',
                  'is_in_shopping_cart')
        model = Recipe

    def get_is_favorited(self, obj):
        user = self.context['request'].user
        if not user.is_authenticated:
            return False
        user_object = get_object_or_404(User, username=user)
        return Favorite.objects.filter(user=user_object, recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context['request'].user
        if not user.is_authenticated:
            return False
        user_object = get_object_or_404(User, username=user)
        return ShoppingCard.objects.filter(user=user_object,
                                           recipe=obj).exists()


class RecipeWriteSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=False)

    class Meta:
        fields = ('id', 'author', 'ingredients', 'tags',
                  'name', 'text', 'cooking_time', 'image')
        model = Recipe

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        tags_data = validated_data.pop('tags')
        image_data = validated_data.pop('image')
        image_content = image_data.read()
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags_data)
        recipe.ingredients.set(ingredients_data)
        recipe.image.save(f'{recipe.name}.jpg',
                          ContentFile(image_content), save=True)
        create_ingredients(self.context['ingredients'], recipe)
        return recipe

    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        tags_data = validated_data.pop('tags')
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get('cooking_time',
                                                   instance.cooking_time)
        instance.image = validated_data.get('image', instance.image)
        instance.tags.set(tags_data)
        instance.ingredients.set(ingredients_data)
        ingredient_recipes = IngredientsRecipe.objects.filter(recipe=instance)
        ingredients_mapping = {ingredient['id']: ingredient for
                               ingredient in self.context['ingredients']}

        with transaction.atomic():
            for ingredient_recipe in ingredient_recipes:
                amount = ingredients_mapping.get(ingredient_recipe.
                                                 ingredient_id,
                                                 {}).get('amount')
                if amount is not None:
                    ingredient_recipe.amount = amount
                    ingredient_recipe.save()
            new_ingredient_recipes = [
                IngredientsRecipe(
                    recipe=instance,
                    ingredient_id=ingredient['id'],
                    amount=ingredient.get('amount')
                )
                for ingredient in self.context['ingredients']
                if ingredient['id'] not in ingredients_mapping
            ]
            IngredientsRecipe.objects.bulk_create(new_ingredient_recipes)
        return instance


class SubscribeRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class SubscribeListSerializer(serializers.ModelSerializer):
    email = serializers.CharField(
        source='author.email',
        read_only=True)
    id = serializers.IntegerField(
        source='author.id',
        read_only=True)
    username = serializers.CharField(
        source='author.username',
        read_only=True)
    first_name = serializers.CharField(
        source='author.first_name',
        read_only=True)
    last_name = serializers.CharField(
        source='author.last_name',
        read_only=True)
    recipes = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()
    recipes_count = serializers.ReadOnlyField(
        source='author.recipes.count')

    class Meta:
        model = Subscribe
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed', 'recipes', 'recipes_count',)

    def get_recipes(self, obj):
        recipes = obj.author.recipes.all()
        return SubscribeRecipeSerializer(
            recipes,
            many=True).data

    def get_is_subscribed(self, obj):
        subscribe = Subscribe.objects.filter(
            user=self.context.get('request').user,
            author=obj.author
        )
        if subscribe:
            return True
        return False


class SubscribeCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscribe
        fields = ('author', )


class ShoppingCartSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(
        source='recipe.id',
    )
    name = serializers.ReadOnlyField(
        source='recipe.name',
    )
    image = serializers.CharField(
        source='recipe.image',
        read_only=True,
    )
    cooking_time = serializers.ReadOnlyField(
        source='recipe.cooking_time',
    )

    class Meta:
        model = ShoppingCard
        fields = ('id', 'name', 'image', 'cooking_time')


class FavoriteSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    name = serializers.ReadOnlyField()
    image = serializers.CharField(
        read_only=True,
    )
    cooking_time = serializers.ReadOnlyField()

    class Meta:
        model = Favorite
        fields = ('id', 'name', 'image', 'cooking_time')
