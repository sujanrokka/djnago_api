from rest_framework import serializers
from .models import Recipe


# class RecipeSerializer(serializers.Serializer):

class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields='__all__'