from django.contrib import admin
from cooking.models import IngredientType, Ingredient, Token, History, Recipe

admin.site.register(IngredientType)
admin.site.register(Ingredient)
admin.site.register(Recipe)

class TokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'token')

admin.site.register(Token, TokenAdmin)

admin.site.register(History)
