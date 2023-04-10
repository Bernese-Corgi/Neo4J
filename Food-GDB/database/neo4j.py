from fastapi import FastAPI
from neo4j import GraphDatabase, basic_auth

# with GraphDatabase.driver(URI, auth=AUTH) as driver:
#     driver.verify_connectivity()

class Neo4jConnection:
    def __init__(self, app: FastAPI = None):
        self.driver = None
        self.session = None
        
        if app != None:
            self.init_app(app=app)

    def init_app(self, app: FastAPI):
        def get_neo4j_driver():
            uri = "bolt://localhost:7687"
            auth = basic_auth("neo4j", "marcella")
            return GraphDatabase.driver(uri, auth=auth)
        
        @app.on_event("startup")
        async def startup_event():
            app.state.neo4j_driver = get_neo4j_driver()

        @app.on_event("shutdown")
        async def shutdown_event():
            await app.state.neo4j_driver.close()

    
    def close(self):
        self.driver.close()

neo4j = Neo4jConnection()