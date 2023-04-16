from fastapi import APIRouter

from service.recipe import RecipeService


router = APIRouter()

@router.get(
    "/ingredients/{recipe_id}"
)
async def get_ingredients(recipe_id: int):
    recipe = RecipeService()
    result = recipe.get_ingredients_by_recipe_id(recipe_id)

    return result