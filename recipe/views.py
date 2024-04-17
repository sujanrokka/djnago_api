from django.shortcuts import render
from .serializers import RecipeSerializer

from rest_framework.decorators import api_view
from .models import Recipe
from rest_framework.response import Response

@api_view()
def hello(request):
    return Response({"data": "Hello, world!"})

@api_view(['GET','POST'])
def list_recipe(request):
    if request.method=='POST':
        print(request.data)
        recipe_serializer=RecipeSerializer(data=request.data)
        recipe=RecipeSerializer.create(request.data)
        print(recipe)
        return Response({
            'data':"CREATED"
            
        })
    else:
        recipes=Recipe.objects.all()
        serializer=RecipeSerializer(recipes,many=True)
        return Response(serializer.data)

  
  
  
    
    # data=[
         
    # ]
    # return Response({
        
    # })