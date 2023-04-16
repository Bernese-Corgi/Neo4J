from fastapi import FastAPI, Depends
from database.neo4j import neo4j_db
from router import food, recipe

def start_server():
    app = FastAPI()

    neo4j_db.init_app(app)

    app.include_router(
        router=food.router,
        prefix="/food",
        tags=["food"],
        dependencies=[Depends(neo4j_db.get_session)]
    )    

    app.include_router(
        router=recipe.router,
        prefix="/recipe",
        tags=["recipe"],
        dependencies=[Depends(neo4j_db.get_session)]
    )    

    return app

app = start_server()