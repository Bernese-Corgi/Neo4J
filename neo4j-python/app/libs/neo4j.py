from typing import Union
from decouple import config
from neo4j import GraphDatabase

class Neo4j:
    def __init__(self):
        uri = config('NEO4J_DB_URI')
        user = config('NEO4J_DB_USER')
        password = config('NEO4J_DB_PASSWORD')
        
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def tx_function(self, tx, query: str, params: dict):
        result = tx.run(query, params)

        records = list(result)
        # summary = result.consume()

        return records
    
    def execute_write(
        self, 
        query: str,
        params: Union[dict, None] = None,
        database = "neo4j"
    ):
        with self.driver.session(database=database) as session:
            result = session.execute_write(self.tx_function, query, params)
        
        return result
    
    def execute_read(
        self, 
        query: str,
        params: Union[dict, None] = None,
        database: str = "neo4j"
    ):
        with self.driver.session(database=database) as session:
            result = session.execute_read(self.tx_function, query, params)
        
        return result
    