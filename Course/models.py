
from django.db import models

class Course(models.Model):
    title=models.CharField(max_length=100)
    description=models.TextField(max_length=1000)
    credit_hr=models.IntegerField()
    def __str__(self):
        return self.title
    
class Subject(models.Model):
    title=models.CharField(max_length=100)
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title
    