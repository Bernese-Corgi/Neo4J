from fastapi import FastAPI
from database.neo4j import neo4j_db

def start_server():
    app = FastAPI()

    neo4j_db.init_app(app)
    

    return app

app = start_server()