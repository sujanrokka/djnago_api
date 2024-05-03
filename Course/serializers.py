from rest_framework import serializers
from .models import Course,Subject,Student

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields='__all__'
     
class CourseDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields='__all__'

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields='__all__'
    
class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields='__all__'