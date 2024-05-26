from django.urls import path,include
from recipe import views
from rest_framework.routers import DefaultRouter



router = DefaultRouter()
router.register('recipeviewset',views.RecipeViewSet,basename='recipeviewset')
router.register('productviewset',views.ProductViewSet,basename='products')


urlpatterns = [
    path('api-auth/',include('rest_framework.urls')),
    path('hello/',views.hello),
    path('recipes/',views.list_recipe),
    path('recipes/<int:id>/',views.recipe_detail),
    path('product/',views.list_product),
    path('product/<int:id>/',views.product_detail),
    path('api/',include(router.urls)),
    path('recipe_c/',views.RecipeListView.as_view()),
    path('recipe_c/<int:id>/',views.RecipeDetailView.as_view()),
    path('send_mail/',views.mail_user),
    path('contact/',views.handle_contact),
    path('contacts/', views.ContactAPIView.as_view(), name='contact_api'),
    path("uploadcsv/",views.upload_ingredient_csv,name='upload'),
    path("downloadrcsv/",views.export_recipe,name='download'),
    path('dashboard/',views.dashboard,name="dashboard"),
    
]
