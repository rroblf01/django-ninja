from djangoninja.schemas import Message
from cooking.models import Recipe
from cooking.schemas import RecipeSchema, RecipeInSchema
from cooking.utils import create_history
from ninja import Router
from typing import List


router = Router()

@router.get("/", response={200: List[RecipeSchema]})
def list_recipes(request):
    recipes = list(Recipe.objects.all())

    response = 200, recipes
    
    create_history(request, response)
    return response


@router.get("/{recipent_id}", response={200: RecipeSchema, 404: Message})
def get_recipe(request, recipent_id: int):
    try:
        response = 200, Recipe.objects.get(id=recipent_id)
    except Recipe.DoesNotExist:
        response = 404 ,{"message": "Recipe not found"}
    
    create_history(request, response)
    return response


@router.post("/", response={201: RecipeSchema, 409: Message})
def create_recipe(request, payload: RecipeInSchema):
    if Recipe.objects.filter(name__iexact=payload.name).exists():
        response =  409, {"message": "Recipe already exists"}
    else:
        response = 201, Recipe.objects.create(**payload.dict())

    create_history(request, response)
    return response


@router.put("/{recipent_id}", response={200: RecipeSchema, 404: Message})
def update_recipe(request, recipent_id: int, payload: RecipeInSchema):
    if Recipe.objects.filter(name__iexact=payload.name).exclude(id=recipent_id).exists():
        response =  409, {"message": "Recipe with same name already exists"}
    else:
        try:
            recipe = Recipe.objects.get(id=recipent_id)
            recipe.update(**payload.dict())

            response = 200, recipe
        except Recipe.DoesNotExist:
            response = 404, {"message": "Recipe not found"}

    create_history(request, response)
    return response


@router.delete("/{recipent_id}", response={204: Message, 404: Message})
def delete_recipe(request, recipent_id: int):
    try:
        Recipe.objects.get(id=recipent_id).delete()
        response = 204, {"message": "Recipe deleted"}
    except Recipe.DoesNotExist:
        response = 404, {"message": "Recipe not found"}

    create_history(request, response)
    return response

@router.get("/{ingredient_id}", response={200: List[RecipeSchema], 404: Message})
def get_recipies_by_ingredient(request, ingredient_id: int):
    recipies = Recipe.objects.filter(ingredients__ingredient_type__id=ingredient_id)
    if not recipies:
        response = 404 ,{"message": "Recipe not found"}
    else:
        response = 200, recipies
    
    create_history(request, response)
    return response