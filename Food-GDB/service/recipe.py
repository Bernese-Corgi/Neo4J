from collections import defaultdict
from database.neo4j import neo4j_db

class RecipeService:
    def __init__(self) -> None:
        pass

    def get_ingredients_by_recipe_id(self, id: int):
        neo_result = neo4j_db.execute_read(
            query="""
                MATCH (r:Recipe { recipe_id: $id })
                OPTIONAL MATCH (r)-[m:MADE_BY]->(i:Ingredient)
                RETURN r.recipe_id, m.type, m.amount, i.name
            """,
            params={ "id": id }
        )
        
        ingredients = defaultdict(dict)
        
        for row in neo_result:
            key = row.get("r.recipe_id")
            ing_type = row.get("m.type")
            ingredients[key]["recipe_id"] = row.get("r.recipe_id")
            ingredients[key][ing_type] = [
                    *ingredients[key].get(ing_type, []),
                    f"{row.get('i.name')} {row.get('m.amount')}"
                ]

        return list(ingredients.values())
    
    def get_similar_ingredients_by_recipe_id(
            self,
            id: int,
            only_main: bool,
            same_amt: bool
    ):
        query="""
            MATCH (r:Recipe { recipe_id: $id })
            MATCH (r)-[m:MADE_BY]->(i:Ingredient)
            WHERE m.type_code = '3060001' // 주재료
            MATCH (i)<-[m2:MADE_BY]-(r2:Recipe)
        """

        condition = {
            "only_main": {
                "query": " m2.type_code = '3060001' ",
                "cond": only_main
            },
            "same_amt": {
                "query": " m2.amount = m.amount ",
                "cond": same_amt
            }
        }

        for i, val in enumerate([item for _, item in condition.items() if item['cond'] != False]):
            print(i)
            query += " WHERE " if i == 0 else " AND "
            query += val["query"]
        
        query += " RETURN r.recipe_id, i.name, m2.type, m2.amount, r2.recipe_id"

        neo_result = neo4j_db.execute_read(
            query=query,
            params={ "id": id }
        )

        ingredients = defaultdict(dict)

        for row in neo_result:
            key = row.get('r.recipe_id')
            ing_name = row.get('i.name')
            ingredients[key]["recipe_id"] = row.get('r.recipe_id')
            ingredients[key][ing_name] = [
                *ingredients[key].get(ing_name, []),
                {
                    "another recipe id": row.get("r2.recipe_id"),
                    "type": row.get("m2.type"),
                    "amount": row.get("m2.amount")
                }
            ]

        return list(ingredients.values())