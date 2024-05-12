from django.http import HttpResponse
from django.shortcuts import render
from .serializers import RecipeSerializer,ProductSerializer,RecipeListSerializer,RecipeCreateSerializer
from rest_framework.decorators import api_view,permission_classes,authentication_classes
from rest_framework.permissions import IsAuthenticated
from .models import Recipe,Product
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token

#-------------------------------------------------------------------------------------------------for mail
from django.conf import settings
from django.core.mail import send_mail

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def mail_user(request):
    subject = 'welcome to GFG world'
    message = 'Hi  thank you for registering in geeksforgeeks.'
    html_message="<h1> welcome to our website</h1> <p>You have logged in from <strong>{ip_address} </strong> </p> <a href=\"google.com\" style=\"text-decoration:none; padding:10px; background-color:cyan;\">Visit </a>"
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['tiwarianimika2000@gmail.com']
    send_mail( subject, message,html_message=html_message,recipient_list=recipient_list,from_email=email_from )
    return HttpResponse()


#------------------------------------------------------------------------------------------------------------
class RecipeViewSet(ModelViewSet):
    permission_classes=[IsAuthenticated]
    queryset=Recipe.objects.all()
    serializer_class=RecipeSerializer


class ProductViewSet(ModelViewSet):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer 
    
#-----------------------------------------------------------------------------------------------------------------
  
class RecipeListView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        title=request.query_params.get('title')
        print(title)
        if title is not None:
            recipes=Recipe.objects.filter(title__icontains=title,user=request.user)
        else:
             recipes=Recipe.objects.filter(user=request.user)
        recipe_serializer=RecipeListSerializer(recipes,many=True)
        return Response(recipe_serializer.data)
    
    def post(self,request):
        recipe_serializer=RecipeCreateSerializer(data=request.data)
        recipe_serializer.is_valid(raise_exception=True)
        recipe_serializer.save(user=request.user)
        return Response(recipe_serializer.data,status=201)  

class RecipeDetailView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,*args,**kwargs):
        id=self.kwargs.get('id')
        print(id)
        try:
            recipe=Recipe.objects.get(id=id)
        except Recipe.DoesNotExist:
            return Response({"error":"Recipe not found"},status=404)
        recipe_serializer=RecipeSerializer(recipe)
        return Response(recipe_serializer.data)
    
    def put(self,request,*args,**kwargs):
        id=kwargs.get('id')
        recipe=Recipe.objects.get(id=id)
        recipe_serializer=RecipeSerializer(recipe,data=request.data)
        if recipe_serializer.is_valid():
            recipe_serializer.save(updated_by=request.user)
            return Response(recipe_serializer.data)
        else:
            print(recipe_serializer.errors)
            return Response(recipe_serializer.errors)
        
    def delete(self,request,*args,**kwargs):
        id=kwargs.get('id')
        try:
            recipe=Recipe.objects.get(id=id)
        except Recipe.DoesNotExist:
            return Response(status=404)
        recipe.delete()
        return Response(status=204) 
    
    

    
    
     
class RecipeUpdateView(APIView):
    permission_classes=[IsAuthenticated]
    def put(self,request,*args,**kwargs):
        id=kwargs.get('id')
        recipe=Recipe.objects.get(id=id)
        recipe_serializer=RecipeSerializer(recipe,data=request.data)
        if recipe_serializer.is_valid():
            recipe_serializer.save()
            return Response(recipe_serializer.data)
        else:
            print(recipe_serializer.errors)
            return Response(recipe_serializer.errors)
    def delete(self,request,*args,**kwargs):
        id=kwargs.get('id')
        try:
            recipe=Recipe.objects.get(id=id)
        except Recipe.DoesNotExist:
            return Response(status=404)
        recipe.delete()
        return Response(status=204)


    

# we can do this way also
@api_view()
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def hello(request):
    return Response({"data": "Hello, world!"})


 

@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def list_recipe(request):
    if request.method=='POST':
        print(request.data)
        recipe_serializer=RecipeCreateSerializer(data=request.data)
        
        if recipe_serializer.is_valid(raise_exception=True):
            recipe_serializer.save(user=request.user)
            # recipe_serializer.save()
            # validated_data=recipe_serializer.validated_data
            # recipe=Recipe(user=request.user,**validated_data)
            # recipe.save()
            # recipe_serializer=RecipeCreateSerializer(recipe)
            return Response(recipe_serializer.data,status=201)     
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
        # to get
        # recipe=Recipe.objects.get(id=id)
        recipe_serializer=RecipeSerializer(recipe)
        return Response(recipe_serializer.data)
    
    
    elif request.method=="PUT":
        # to update
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
  