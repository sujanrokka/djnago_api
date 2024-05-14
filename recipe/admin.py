from django.contrib import admin

# Register your models here.
from .models import *
class RecipeAdmin(admin.ModelAdmin):
    list_display=('title','description','time_required')
    search_fields=('title',)
    list_filter=('user',)

admin.site.register(Recipe,RecipeAdmin)
admin.site.register(Ingredient)
admin.site.register(Product)
