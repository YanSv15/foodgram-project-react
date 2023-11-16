from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField
from django.shortcuts import get_object_or_404

from posts.models import (Tag, Ingredient, Recipe, IngredientsRecipe,
                          Favorite, ShoppingCard, TagRecipe, Follow)
from users.models import User
from posts import validators

from django.core.files.base import ContentFile
import base64


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=150,
        required=True,
        validators=(validators.validate_username, ),
    )
    email = serializers.EmailField(
        max_length=254,
        required=True,
    )

    class Meta:
        model = User
        fields = (
            'email',
            'username',
        )


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
    id = serializers.IntegerField(
    )
    measurement_unit = serializers.CharField(
    )
    name = serializers.CharField(
    )

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
        fields = ('id', 'author', 'ingredients', 'tags',
                  'name', 'text', 'cooking_time', 'is_favorited',
                  'is_in_shopping_cart')
        model = Recipe

    def get_is_favorited(self, obj):
        username = self.context['request'].user
        if not username.is_authenticated:
            return False
        user = get_object_or_404(User, username=username)
        return Favorite.objects.filter(user=user, recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        username = self.context['request'].user
        if not username.is_authenticated:
            return False
        user = get_object_or_404(User, username=username)
        return ShoppingCard.objects.filter(user=user, recipe=obj).exists()


class RecipeWriteSerializer(serializers.ModelSerializer):
    image = Base64ImageField(
    )

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
        recipe.image.save(image_data.name, ContentFile(base64.b64decode(image_content)))
        return recipe

    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        tags_data = validated_data.pop('tags')
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get('cooking_time', instance.cooking_time)
        instance.image = validated_data.get('image', instance.image)
        instance.tags.set(tags_data)
        instance.ingredients.set(ingredients_data)
        instance.save()
        return instance

        # for ingredient_data in ingredients_data:
            # ingredient, created = Ingredient.objects.get_or_create(id=ingredient_data['id'])
            # instance.ingredients.add(ingredient)

        # for tag_data in tags_data:
            # tag, created = Tag.objects.get_or_create(id=tag_data['id'])
            # instance.tags.add(tag)


    # def create(self, validated_data):
        # if 'ingredients' not in self.initial_data:
            # recipe = Recipe.objects.create(**validated_data)
            # return recipe
        # ingredients = validated_data.pop('ingredients')
        # recipe = Recipe.objects.create(**validated_data)
        # for ingredient in ingredients:
            # current_ingredient, status = Ingredient.objects.get_or_create(
                # **ingredient
            # )
            # IngredientsRecipe.objects.create(
                # ingredient=current_ingredient, recipe=recipe
            # )
        # return recipe
        # image = validated_data.pop('image')
        # ingredients = validated_data.pop('ingredients')
        # tags = validated_data.pop('tags')
        # recipe = Recipe.objects.create(**validated_data)
        # recipe.tags.set(tags)
        # for tag in tags:
            # TagRecipe.objects.create(tag=tag, recipe=recipe)
        # for ingredient in ingredients:
            # IngredientsRecipe.objects.create(ingredient=ingredient, recipe=recipe)
        # return recipe

        # self.create_ingredients(ingredients_data, recipe)
        # return recipe


class FollowSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(
        source='author.id'
    )
    email = serializers.ReadOnlyField(
        source='author.email'
    )
    username = serializers.ReadOnlyField(
        source='author.username'
    )
    first_name = serializers.ReadOnlyField(
        source='author.first_name'
    )
    last_name = serializers.ReadOnlyField(
        source='author.last_name'
    )
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = Follow
        fields = ('id', 'email', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count')

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj.author).count()


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


class FavoriteRecipeSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(
        source='favorite_recipe.id',
    )
    name = serializers.ReadOnlyField(
        source='favorite_recipe.name',
    )
    image = serializers.CharField(
        source='favorite_recipe.image',
        read_only=True,
    )
    cooking_time = serializers.ReadOnlyField(
        source='favorite_recipe.cooking_time',
    )

    class Meta:
        model = Favorite
        fields = ('id', 'name', 'image', 'cooking_time')
