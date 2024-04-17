from django.db import models

# Create your models here.
class Recipe(models.Model):
    title=models.CharField(max_length=23)
    description=models.TextField()
    time_required=models.CharField(max_length=23)
    
    def __str__(self):
        return self.title
