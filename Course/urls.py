from django.urls import path,include
from . import views

urlpatterns = [
    path('courses/',views.CourseListView.as_view()),
    path('studentbycourse/<int:id>',views.DisplayStudent.as_view()),
    path('students/',views.StudentListView.as_view()),
    path('students_p/',views.StudentListAPIView.as_view()),
    path('subjects/',views.SubjectListView.as_view()),
     
]
