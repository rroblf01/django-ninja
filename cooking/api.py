from cooking.router.ingredient import router as ingredient_router
from cooking.router.recipe import router as recipe_router
from ninja import Router

router = Router()

router.add_router("/ingredients", ingredient_router, tags=["ingredients"])
router.add_router("/recipes", recipe_router, tags=["recipes"])