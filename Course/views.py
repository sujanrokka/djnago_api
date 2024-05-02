from django.shortcuts import render
from .serializers import CourseSerializer,CourseDetailSerializer
from .models import Course,Subject
from rest_framework.response import Response
from rest_framework.views import APIView


class CourseListView(APIView):
    def get(self,request):
        title=request.query_params.get('title')
        print(title)
        if title is not None:
            recipes=Course.objects.filter(title__icontains=title)
        else:
             course=Course.objects.filter(user=request.user)
             serializer=CourseSerializer(recipes,many=True)
        return Response(serializer.data)
    
    def post(self,request):
        recipe_serializer=CourseSerializer(data=request.data)
        recipe_serializer.is_valid(raise_exception=True)
        recipe_serializer.save(user=request.user)
        return Response(recipe_serializer.data,status=201)  



