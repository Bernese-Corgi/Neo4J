import os

from fastapi import FastAPI
from neo4j import GraphDatabase, Session

class Neo4jConnection:
    def __init__(self, app: FastAPI = None) -> None:
        self.driver = None
        
        if app != None:
            self.init_driver(app=app)
    
    # driver의 인스턴스를 만들고 할당한다.
    def init_driver(self, app: FastAPI):
        uri = os.environ['NEO4J_DB_URI']
        username = os.environ['NEO4J_DB_USER']
        password = os.environ['NEO4J_DB_PASSWORD']
        
        # Create an instance of the driver : 드라이버 인스턴스 생성
        self.driver = GraphDatabase.driver(uri, username, password)

        # Verify Connectivity : 새로 생성된 드라이버 인스턴스를 반환하기 전에 연결 세부 정보가 올바른지 확인
        self.driver.verify_connectivity()
        
        

        @app.on_event("startup")
        def startup_event():
            print(f"app startup - neo4j driver stated? {self.driver}")
        
        @app.on_event("shutdown")
        def shutdwon_event():
            if self.driver != None:
                self.driver.close()
                self.driver = None
                print('app shutdown - neo4j driver closed')
    
    def get_driver(self):
        return self.driver
    
    @property
    def session(self):
        return self.driver.session()

neo4j = Neo4jConnection()