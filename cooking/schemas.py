from cooking.models import IngredientType, Ingredient, Recipe
from ninja import ModelSchema

class IngredientTypeSchema(ModelSchema):
    class Meta:
        model = IngredientType
        fields = "__all__"

class IngredientTypeInSchema(ModelSchema):
    class Meta:
        model = IngredientType
        exclude = ["id"]

class IngredientSchema(ModelSchema):
    ingredient_type: IngredientTypeSchema
    class Meta:
        model = Ingredient
        fields = "__all__"

class RecipeSchema(ModelSchema):
    ingredients: list[IngredientSchema]
    class Meta:
        model = Recipe
        fields = "__all__"

class RecipeInSchema(ModelSchema):
    class Meta:
        model = Recipe
        exclude = ["id"]