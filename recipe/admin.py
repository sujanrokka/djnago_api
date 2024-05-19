from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .resources import RecipeResources
# Register your models here.
from .models import *
class RecipeAdmin(ImportExportModelAdmin):
    resource_classess=[RecipeResources]
    list_display=('title','description','time_required')
    search_fields=('title',)
    list_filter=('user',)

admin.site.register(Recipe,RecipeAdmin)
admin.site.register(Ingredient)
admin.site.register(Product)
