from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

from app.router import people, product

app = FastAPI()

app.include_router(people.router, prefix='/people')
app.include_router(product.router, prefix='/product')