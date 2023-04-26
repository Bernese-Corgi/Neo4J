# Transaction

세션을 통해 하나 이상의 트랜잭션을 실행할 수 있다.

트랜잭션은 데이터베이스에 대해 수행되는 작업단위로 구성된다.
다른 트랜잭션과 독립적으로 일관되고 신뢰할 수 있는 방식으로 처리된다.

**ACID 트랜잭션**

정의에 따르면, 트랜잭션은 원자성/일관성/격리성/내구성이 있어야 한다.

많은 개발자가 관계형 데이터베이스 작업을 통해 ACID 트랜잭션에 익숙하므로, ACID 일관성 모델이 한동안 표준이었다.

## 트랜잭션 유형

드라이버에 의해 노출되는 세 가지 유형의 트랜잭션이 있다.

### 트랜잭션 auto commit

자동 커밋 트랜잭션은 DBMS에 대해 즉시 실행되고, 즉시 승인되는 단일 작업 단위이다.

세션 객체에서 `run()` 메서드를 호출하고, cypher 문과 매개변수를 전달하여 실행할 수 있다.

```py
session.run(
    "MATCH (p:Person {name: $name}) RETURN p", # Query
    name="Tom Hanks" # Named parameters referenced
)                    # in Cypher by prefixing with a $
```

> **일회성 쿼리 전용**
>
> 쿼리를 실행할 때 일시적인 오류가 있는 경우, 드라이버는 `session.run()`을 사용할 때 쿼리를 다시 시도하지 않는다.
> 그러므로, 이러한 쿼리는 일회성 쿼리에만 사용해야 하며, 프로덕션에는 사용하면 안된다.

### 트랜잭션 읽기

Neo4j에서 데이터를 읽으려면, 읽기 트랜잭션을 실행해야 한다.

클러스터 환경에서 읽기 쿼리는 클러스터 전체에 분산된다.

세션은 작업단위를 나타내는 함수인 단일 매개변수를 기대하는 `execute_read()` 함수를 제공한다.

**execute_read()**

*첫번째 인수*
- 콜백 함수. 
- 콜백함수 내 첫번째 인수(tx) : 트랜잭션 객체. `.run()` 함수를 호출하여 cypher를 실행할 수 있다.

```py
# Define a Unit of work to run within a Transaction (`tx`)
def get_movies(tx, title):
    return tx.run("""
        MATCH (p:Person)-[:ACTED_IN]->(m:Movie)
        WHERE m.title = $title // (1)
        RETURN p.name AS name
        LIMIT 10
    """, title=title)

# Execute get_movies within a Read Transaction
session.execute_read(get_movies,
    title="Arthur" # (2)
)
```