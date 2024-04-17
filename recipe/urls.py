from django.urls import path,include
from recipe import views

urlpatterns = [
    path('api-auth/',include('rest_framework.urls')),
    path('hello/',views.hello),
    path('recipes/',views.list_recipe),
]
