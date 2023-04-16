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
            print(row)
            key = row.get("r.recipe_id")
            ing_type = row.get("m.type")
            ingredients[key]["recipe_id"] = row.get("r.recipe_id")
            ingredients[key][ing_type] = [
                    *ingredients[key].get(ing_type, []),
                    f"{row.get('i.name')} {row.get('m.amount')}"
                ]

        return list(ingredients.values())