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

    def execute_write(self, *args):
        with self.driver.session() as session:
            result = session.execute_write(*args)
        
        records = list(result)
        summary = result.consume()
        
        return records, summary

    def execute_read(self, *args):
        with self.driver.session() as session:
            result = session.execute_read(*args)
        
        records = list(result)
        summary = result.consume()
        
        return records, summary
    