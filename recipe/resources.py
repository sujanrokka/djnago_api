from import_export import resources
from .models import Recipe

class RecipeResources(resources.ModelResource):
    class Meta:
        model = Recipe
        fields=('id','ingredients','title','description','time','difficulty','rating','user__username')