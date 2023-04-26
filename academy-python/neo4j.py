from neo4j import GraphDatabase


class Neo4jConnection:

    def init_driver(self, uri, username, password):
        # Create an instance of the driver : 드라이버 인스턴스 생성
        self.driver = GraphDatabase.driver(uri, username, password)

        # # Verify Connectivity : 새로 생성된 드라이버 인스턴스를 반환하기 전에 연결 세부 정보가 올바른지 확인
        self.driver.verify_connectivity()

        return self.driver
    
    def get_driver(self):
        return self.driver