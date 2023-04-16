from fastapi import APIRouter, Depends

from service.translate import TranslateService


router = APIRouter()

@router.post(
    path="/ingredients"
)
async def insert_ingredients():
    translate = TranslateService()
    result = translate.insert_ingredients()
    return result