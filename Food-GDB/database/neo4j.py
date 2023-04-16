from typing import Union
from fastapi import FastAPI
from neo4j import GraphDatabase

class Neo4jConnection:
    def __init__(self, app: FastAPI = None):
        self._driver = None
        self._session = None

        if app != None:
            self.init_app(app)

    def get_driver(self):
        uri = "bolt://localhost:7687"
        user = "neo4j"
        password = "marcella"
        return GraphDatabase.driver(uri, auth=(user, password))

    def get_session(self):
        return self._driver.session(database="neo4j")
    
    def tx_func(self, tx, query: str, params: dict):
        result = tx.run(query, params)
        return list(result)
    
    def execute_write(self, query: str, params: Union[dict, None] = None):
        if self._session != None:
            with self._session() as s:
                result = s.execute_write(self.tx_func, query, params)
            return result
        else:
            with self.get_session() as session:
                result = session.execute_write(self.tx_func, query, params)
            return result

    def execute_read(self, query: str, params: Union[dict, None] = None):
        if self._session != None:
            with self._session() as s:
                result = s.execute_read(self.tx_func, query, params)
            return result
        else:
            with self.get_session() as session:
                result = session.execute_read(self.tx_func, query, params)
            return result
    
    def init_app(self, app: FastAPI):
        self._driver = self.get_driver()

        @app.on_event("startup")
        async def startup_event():
            if self._driver == None:
                self._driver = self.get_driver()

        @app.on_event("shutdown")
        async def shutdown_event():
            self._session.close()
            self._driver.close()

neo4j_db = Neo4jConnection()