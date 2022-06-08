"""
Sesrializers for recipe APIs
"""

from rest_framework import serializers

from core.models import (
    Recipe,
    Tag,
    Ingredient
    )
class IngredientSerializer(serializers.ModelSerializer):
    """Serializer for ingredient"""
    class Meta:
        model = Ingredient
        fields = ['id', 'name']
        read_only_fields = ['id']

class TagSerializer(serializers.ModelSerializer):
    """
    Serializer for tags.
    """
    class Meta:
        model = Tag
        fields = ['id', 'name']
        read_only_fields = ['id']

class RecipeSerializer(serializers.ModelSerializer):
    """
    Serializer for recipe
    """
    tags = TagSerializer(many=True, required=False) # a list of items 
    ingredients = IngredientSerializer(many=True, required=False)
    class Meta:
        model = Recipe
        fields = [
            'id', 'title', 'time_minutes', 'price', 'link', 'tags',
            'ingredients'
            ]
        read_only_fields = ['id']
    def _get_or_create_tags(self, tags, recipe):
        """Handle getting or creating tags as needed"""
        auth_user = self.context['request'].user
        for tag in tags:
            tag_obj, created = Tag.objects.get_or_create(
                user=auth_user,
                **tag, # future proof 
            )
            recipe.tags.add(tag_obj)
    def _get_or_create_ingredients(self, ingredients,recipe):
        """Handle getting or creating ingredients as needed"""
        auth_user = self.context['request'].user
        for ingredient in ingredients:
            ingredient_obj, created = Ingredient.objects.get_or_create(
                user=auth_user,
                **ingredient, # future proof 
            )
            recipe.ingredients.add(ingredient_obj)
    def create(self, validated_data):
        """
        Create a Recipe
        """
        tags = validated_data.pop('tags', []) # defaults to []
        ingredients = validated_data.pop('ingredients', []) # defaults to []
        recipe = Recipe.objects.create(**validated_data)
        self._get_or_create_tags(tags, recipe)
        self._get_or_create_ingredients(ingredients, recipe)  
        
        return recipe

    def update(self, instance, validated_data):
        """Update a recipe."""
        tags = validated_data.pop('tags', None) # defaults to []
        if tags is not None:
            instance.tags.clear()
            self._get_or_create_tags(tags, instance)
        if ingredients is not None: # to allow empty list to go through to clear
            instance.ingredients.clear()
            self._get_or_create_ingredients(ingredients, instance)

        for attr,value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()

        return instance
class RecipeDetailSerializer(RecipeSerializer):
    """Serializer for recipe detail view. """

    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ['description']
class RecipeImageSerializer(serializers.ModelSerializer):
    """Serializer for uploading images to recipes"""

    class Meta:
        model = Recipe
        fields = ['id', 'image']
        read_only_fields = ['id']
        extra_kwargs = {'image': {'required':'True'}}



    

