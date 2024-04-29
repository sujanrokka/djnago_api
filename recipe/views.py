from django.shortcuts import render
from .serializers import RecipeSerializer,ProductSerializer

from rest_framework.decorators import api_view
from .models import Recipe,Product
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet



class RecipeViewSet(ModelViewSet):
    queryset=Recipe.objects.all()
    serializer_class=RecipeSerializer



class ProductViewSet(ModelViewSet):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer 











# we can do this way also
@api_view()
def hello(request):
    return Response({"data": "Hello, world!"})

@api_view(['GET','POST'])
def list_recipe(request):
    if request.method=='POST':
        print(request.data)
        recipe_serializer=RecipeSerializer(data=request.data)
        
        if recipe_serializer.is_valid():
            recipe_serializer.save()
            return Response(recipe_serializer.data)     
        else:
            print(recipe_serializer.errors)
            return Response(recipe_serializer.errors)
    
    recipes=Recipe.objects.all()
    serializer=RecipeSerializer(recipes,many=True)
    return Response(serializer.data,status=201)


@api_view(['GET','DELETE','PUT'])
def recipe_detail(request,id):
    try:
        recipe=Recipe.objects.get(id=id)
    except Recipe.DoesNotExist:
        return Response(status=404)
    
    if request.method=='GET':
        # recipe=Recipe.objects.get(id=id)
        recipe_serializer=RecipeSerializer(recipe)
        return Response(recipe_serializer.data)
    
    
    
    elif request.method=="PUT":
        #  recipe=Recipe.objects.get(id=id)
         recipe_serializer=RecipeSerializer(recipe,data=request.data)
         if recipe_serializer.is_valid():
            recipe_serializer.save()
            return Response(recipe_serializer.data)
         else:
            print(recipe_serializer.errors)
            return Response(recipe_serializer.errors)
         
         
    
    elif request.method=='DELETE':
        #  recipe=Recipe.objects.get(id=id)
         recipe.delete()
         return Response(status=204)
  
  
  
  

@api_view(['GET','POST'])        
def list_product(request):
    if request.method=='POST':
        print(request.data)
        product_serializer=ProductSerializer(data=request.data)
        
        if product_serializer.is_valid():
            product_serializer.save()
            return Response(product_serializer.data)     
        else:
            print(product_serializer.errors)
            return Response(product_serializer.errors)
    
    products=Product.objects.all()
    serializer=ProductSerializer(products,many=True)
    return Response(serializer.data,status=201)


        
@api_view(['GET','DELETE','PUT'])
def product_detail(request,id):
    try:
        recipe=Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response(status=404)
    if request.method=='GET':
        products=Product.objects.get(id=id)
        product_serializer=ProductSerializer(products)
        return Response(product_serializer.data)
    
    
    elif request.method=="PUT":
         products=Product.objects.get(id=id)
         product_serializer=RecipeSerializer(recipe,data=request.data)
         if product_serializer.is_valid():
            product_serializer.save()
            return Response( product_serializer.data)
         else:
            print( product_serializer.errors)
            return Response(product_serializer.errors)
    
    elif request.method=='DELETE':
         products=Product.objects.get(id=id)
         products.delete()
         return Response(status=204)
  