from djangoninja.schemas import Message
from cooking.models import IngredientType
from cooking.schemas import IngredientTypeSchema, IngredientTypeInSchema
from cooking.utils import create_history
from ninja import Router
from typing import List


router = Router()

@router.get("/", response={200: List[IngredientTypeSchema]})
def list_ingredients(request):
    ingredients = list(IngredientType.objects.all())

    response = 200, ingredients
    
    create_history(request, response)
    return response


@router.get("/{ingredient_id}", response={200: IngredientTypeSchema, 404: Message})
def get_ingredient(request, ingredient_id: int):
    try:
        response = 200, IngredientType.objects.get(id=ingredient_id)
    except IngredientType.DoesNotExist:
        response = 404 ,{"message": "IngredientType not found"}
    
    create_history(request, response)
    return response


@router.post("/", response={201: IngredientTypeSchema, 409: Message})
def create_ingredient(request, payload: IngredientTypeInSchema):
    if IngredientType.objects.filter(name__iexact=payload.name).exists():
        response =  409, {"message": "IngredientType already exists"}
    else:
        response = 201, IngredientType.objects.create(**payload.dict())

    create_history(request, response)
    return response


@router.put("/{ingredient_id}", response={200: IngredientTypeSchema, 404: Message})
def update_ingredient(request, ingredient_id: int, payload: IngredientTypeInSchema):
    if IngredientType.objects.filter(name__iexact=payload.name).exclude(id=ingredient_id).exists():
        response =  409, {"message": "IngredientType with same name already exists"}
    else:
        try:
            ingredient = IngredientType.objects.get(id=ingredient_id)
            ingredient.update(**payload.dict())

            response = 200, ingredient
        except IngredientType.DoesNotExist:
            response = 404, {"message": "IngredientType not found"}

    create_history(request, response)
    return response


@router.delete("/{ingredient_id}", response={204: Message, 404: Message})
def delete_ingredient(request, ingredient_id: int):
    try:
        IngredientType.objects.get(id=ingredient_id).delete()
        response = 204, {"message": "IngredientType deleted"}
    except IngredientType.DoesNotExist:
        response = 404, {"message": "IngredientType not found"}

    create_history(request, response)
    return response
