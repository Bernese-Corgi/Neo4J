from fastapi import APIRouter, Depends
from neo4j import Driver, GraphDatabase

router = APIRouter()

URI = "bolt://localhost:7687"
AUTH = ("marcella", "marcella")


def create_person(tx, name):
    result = tx.run(
        "MERGE (:Person {name: $name})",
        name=name
    )

    summary = result.consume()

    return summary

@router.post('/')
async def post_person():
    with GraphDatabase.driver(URI, auth=AUTH).session(database="people") as session:
        summary = session.execute_write(create_person, name="Marcella")  

        print("Created {nodes_created} nodes in {time} ms.".format(
            nodes_created=summary.counters.nodes_created,
            time=summary.result_available_after
        ))

    return summary