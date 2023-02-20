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

def get_people(tx):
    result = tx.run("MATCH (p:Person) RETURN p")
    records = list(result)
    summary = result.consume()
    return records, summary

@router.get('/')
async def get_person():
    with GraphDatabase.driver(URI, auth=AUTH).session(database="neo4j") as session:
        records, summary = session.execute_read(get_people)

        # Summary information
        print("The query `{query}` returned {records_count} records in {time} ms.".format(
            query=summary.query, records_count=len(records),
            time=summary.result_available_after
        ))

        people = []

        for person in records:
            people = [*people, person.data()]
        
        return people