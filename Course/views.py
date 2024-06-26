from django.shortcuts import render
from .serializers import CourseSerializer,CourseDetailSerializer,SubjectSerializer,StudentSerializer
from .models import Course,Subject,Student
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView #this is genric view for pagination
from rest_framework import generics
from .pagination import LargeResultsSetPagination


class CourseListView(APIView):
    def get(self,request):
        title=request.query_params.get('title')
        print(title)
        if title is not None:
            course=Course.objects.filter(title__icontains=title)
        else:
             course=Course.objects.all()
             serializer=CourseSerializer(course,many=True)
        return Response(serializer.data)
    
    def post(self,request):
        course_serializer=CourseSerializer(data=request.data)
        course_serializer.is_valid(raise_exception=True)
        course_serializer.save()
        return Response(course_serializer.data,status=201)  
    
    
class StudentListView(APIView):
       def get(self,request):
        name=request.query_params.get('name')
        print(name)
        if name is not None:
            student=Student.objects.filter(name__icontains=name)
        else:
             student=Student.objects.all()
             serializer=StudentSerializer(student,many=True)
        return Response(serializer.data)
    
       def post(self,request):
        student_serializer=StudentSerializer(data=request.data)
        student_serializer.is_valid(raise_exception=True)
        student_serializer.save()
        return Response(student_serializer.data,status=201)  
    
class SubjectListView(APIView):
    def get(self,request):
        title=request.query_params.get('title')
        print(title)
        if title is not None:
            course=Course.objects.filter(title__icontains=title)
        else:
             course=Course.objects.all()
             serializer=CourseSerializer(course,many=True)
        return Response(serializer.data)
    
    def post(self,request):
        course_serializer=SubjectSerializer(data=request.data)
        course_serializer.is_valid(raise_exception=True)
        course_serializer.save()
        return Response(course_serializer.data,status=201)  
    
    
#this is for getting students from course
class DisplayStudent(APIView):
   def get(self,request,*args,**kwargs):
        id=kwargs.get('id')
        print(id)
        try:
            course=Course.objects.get(id=id)
            students_in_course=course.students.all()
           
        except Course.DoesNotExist:
            return Response({"error":"Course not found"},status=404)
        student_serializer=StudentSerializer(students_in_course,many=True)
        return Response(student_serializer.data)
        
    
    
#this is for pagination
class StudentListAPIView(ListAPIView):
    # queryset=Student.objects.all()
    queryset=Student.objects.select_related('course') #this is for query optimization
    #many to many field ma prefetch_related query use garne and for foreign key use select_related in forward relation
    serializer_class=StudentSerializer
    pagination_class=LargeResultsSetPagination
    
    
    



