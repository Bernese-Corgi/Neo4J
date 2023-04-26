# Neo4j Connection String

## element

![neo4j url](https://cdn.graphacademy.neo4j.com/assets/img/courses/shared/connection-string.png)

1. **scheme** : Neo4j 인스턴스에 연결하는 데 사용되는 체계. `neo4j`, `neo4j+s`
2. **initial server address** : Neo4j DBMS의 초기 서버 주소.
3. **port** : DBMS가 실행 중인 포트 번호.
4. 추가 연결 구성(예: 라우팅 컨텍스트)

## Scheme

**neo4j**

- DBMS에 대한 암호화되지 않은 연결을 생성합니다. 
- 로컬 DBMS에 연결 중이거나 암호화를 명시적으로 설정하지 않은 경우 이 옵션이 가장 적합할 것입니다.

**neo4j+s**

- DBMS에 대한 암호화된 연결을 생성합니다. 
- 드라이버는 인증서의 진위를 확인하고 인증서에 문제가 있는 경우 연결 확인에 실패합니다.

**neo4j+ssc**

- DBMS에 대한 암호화된 연결을 생성하지만 인증서의 신뢰성을 확인하려고 시도하지 않습니다.

**[bolt scheme]**

- 볼트 체계의 변형을 사용하여 단일 DBMS(클러스터 환경 또는 독립 실행형 내에서)에 직접 연결할 수 있습니다. 
- 이는 데이터 사이언스 또는 분석용으로 구성된 단일 서버가 있는 경우에 유용할 수 있습니다.

**bolt**

- 단일 DBMS에 직접 암호화되지 않은 연결을 생성합니다.

**bolt+s**

- 단일 DBMS에 직접 암호화된 연결을 생성하고 인증서를 확인합니다.

**bolt+ssc**

- 단일 DBMS에 직접 암호화된 연결을 생성하지만 인증서의 신뢰성을 확인하려고 시도하지 않습니다.


## 추가 커넥션 구성

`?` 다음에 연결 문자열에 추가 연결 정보를 추가할 수 있습니다. 
예를 들어 다중 데이터 센터 클러스터에서 지역성을 활용하여 대기 시간을 줄이고 성능을 향상시킬 수 있습니다

이 경우 동일한 데이터 센터 내에 있는 Neo4j 인스턴스에 연결하기 위해 일련의 애플리케이션 서버에 대한 라우팅 정책을 구성할 수 있습니다.

[자세히 보기](https://neo4j.com/developer/kb/consideration-about-routing-tables-on-multi-data-center-deployments/)
