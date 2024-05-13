from rest_framework import serializers
from .models import Recipe,Product,Ingredient,Contact
from django.contrib.auth.models import User


# class RecipeSerializer(serializers.Serializer):
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields=[
           "email",
           "id",  
        ]
     
class RecipeSerializer(serializers.ModelSerializer):
    user=UserSerializer()

    class Meta:
        model = Recipe
        fields='__all__'
     
class RecipeListSerializer(serializers.ModelSerializer):
  
    class Meta:
        model = Recipe
        fields=[
            "id",
            "title",
            "description" ,
             "time_required",
            "difficulty",
            "rating",
            "user",
            "updated_by",
        ]
     
class RecipeCreateSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Recipe
        fields=[
            "title",
            "description" ,
             "time_required",
            "difficulty",
            "rating",
           
        ]
        
class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields='__all__'
        
     
     
        
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields='__all__'
        
    
class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields='__all__'
