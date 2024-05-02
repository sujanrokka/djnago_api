from rest_framework import serializers
from .models import Course,Subject

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields='__all__'
     
class CourseDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields='__all__'