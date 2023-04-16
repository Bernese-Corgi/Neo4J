from typing import Union
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

@router.get(
    "/similar-ingredients/{recipe_id}"
)
async def get_similar_ingredients(
    recipe_id: int, 
    only_main: Union[bool, None] = False,
    same_amt: Union[bool, None] = False
):
    recipe = RecipeService()
    result = recipe.get_similar_ingredients_by_recipe_id(
        recipe_id, 
        only_main,
        same_amt
    )
    return result