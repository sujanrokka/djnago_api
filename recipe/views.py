from ipaddress import ip_address
from django.http import HttpResponse
from django.shortcuts import render
from .serializers import ContactSerializer, RecipeSerializer,ProductSerializer,RecipeListSerializer,RecipeCreateSerializer
from rest_framework.decorators import api_view,permission_classes,authentication_classes
from rest_framework.permissions import IsAuthenticated
from .models import Recipe,Product,Contact,Ingredient
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from .forms import ContactForm
from django.template.loader import render_to_string
from rest_framework import status
from rest_framework.views import APIView
from.serializers import ContactSerializer
import csv
from .resources import RecipeResources
import datetime



def dashboard(request):
    return render(request,'starter.html',)

#------user le download garna csv--------------------------------------------------------------------------------------------------------------------------
def export_recipe(request):
    recipes=Recipe.objects.filter(user=request.user)
    recipe_data=RecipeResources()
    dataset=recipe_data.export(recipes)
    date=datetime.datetime.now()
    response=HttpResponse(dataset.csv,content_type="text/csv")
    response['Content-Disposition']=f'attachment; filename="recipes-{date}.csv"'
    return response



#for csv file uplaod
def upload_ingredient_csv(request):
    if request.method == 'POST':
        ingredient_file = request.FILES['ingredient_file']
        decoded_file = ingredient_file.read().decode('utf-8').splitlines()
        # for line in decoded_file:
        #     print(line)
        reader=csv.DictReader(decoded_file)
        for row in reader:
            print(row['Name'])
            Ingredient.objects.create(name=row['Name'])
        return HttpResponse("file uploaded")
    return render(request,'upload_ingredient_csv.html')
            
        
    
 
#-------------------------------------------------------------------------------------------------for mail sending-------------------
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
    ip_address=get_client_ip(request)
    subject = 'mail aayo mail'
    message = 'Hi  thank you for registering in geeksforgeeks.'
    html_message="<h1> welcome to our website</h1> <p>You have logged in from <strong>{ip_address} </strong> </p> <a href=\"google.com\" style=\"text-decoration:none; padding:10px; background-color:cyan;\">Visit </a>"
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['tiwarianimika2000@gmail.com']
    send_mail( subject, message,html_message=html_message,recipient_list=recipient_list,from_email=email_from )
    return HttpResponse()



#for contact to admin
def handle_contact(request):
   if request.method == 'POST':
        ip_address=get_client_ip(request)
        form = ContactForm(request.POST)
        if form.is_valid():
            contact= form.save()
            subject="New query at : Recipe app"
            message = request.POST.get('query')
            from_email = 'sujanrokka2000@gmail.com'
            recipient_list = ['tiwarianimika2000@gmail.com']
            html_message=render_to_string('email.html',{'ip_address':ip_address,'contact':contact},request)
            send_mail(subject, message, from_email, recipient_list,html_message=html_message)
        return HttpResponse('Email sent successfully')
  
   else:  
        form = ContactForm(request.POST)
        return render(request,'contact.html',{'form':form})  
        
 
 #api for contact us-----------------------------------------------------------------------------------------------------------------------------       
class ContactAPIView(APIView):
    def post(self, request, format=None):
        ip_address = get_client_ip(request)
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            print(serializer.validated_data)
            contact = Contact.objects.create(**serializer.validated_data)
            subject = "New Query at: Recipe app"
            message = serializer.validated_data['query']
            from_email = 'sujanrokka2000@gmail.com'
            recipient_list = ['tiwarianimika2000@gmail.com']
            html_message = render_to_string('email.html', {'ip_address': ip_address, 'contact': contact}, request)

            send_mail(subject, message, from_email, recipient_list, html_message=html_message)
            return Response({"detail": "Email sent successfully!"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"detail": "Invalid form data"}, status=status.HTTP_400_BAD_REQUEST)
        


#----Yo view set use garera-------------------------------------------------------------------------------------------------------------------------
class RecipeViewSet(ModelViewSet):
    permission_classes=[IsAuthenticated]
    queryset=Recipe.objects.all()
    serializer_class=RecipeSerializer


class ProductViewSet(ModelViewSet):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer 
    
#---------------------YO class based views use garera--------------------------------------------------------------------------------------------
  
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


    
    
    
#----------------------------------yo function based views api use garera-------------------------------------------------
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
  
