from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Ingredient(models.Model):
    name=models.CharField(max_length=23)
    def __str__(self):
        return self.name
    
    
class Recipe(models.Model):
    title=models.CharField(max_length=23)
    description=models.TextField()
    time_required=models.CharField(max_length=23)
    difficulty=models.CharField(max_length=20,null=True)
    rating=models.IntegerField(default=0,null=True)
    updated_by=models.ForeignKey(User,on_delete=models.CASCADE,null=True,related_name="updated_by")
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,related_name="created_by")
    ingredients=models.ManyToManyField(Ingredient)
    
    def __str__(self):
        return self.title



class Product(models.Model):
    title=models.CharField(max_length=23)
    description=models.TextField()
    price=models.DecimalField(max_digits=10,decimal_places=2)
    expiry_date=models.DateField()
    
    def __str__(self):
        return self.title
    
    
class Contact(models.Model):
    name=models.CharField(max_length=23)
    address=models.TextField()
    query=models.TextField()
    contact=models.IntegerField()
    email=models.EmailField()
    def __str__(self):
        return self.name