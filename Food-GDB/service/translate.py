from collections import defaultdict
import json
import os

from database.neo4j import neo4j_db

class TranslateService:
    def __init__(self) -> None:
        pass
    
    @staticmethod
    def get_ingredients_json():
        path = os.getcwd() + "/data/ingredients.json"
        with open(path, "rt", encoding="UTF8") as f:
            data = json.load(f)
        
        return data
    
    def insert_ingredients(self):
        data = self.get_ingredients_json()

        recipes = defaultdict(dict)
        
        for ing in data:
            key = ing["RECIPE_ID"]
            recipes[key] = {
                "recipe_id": key,
                "ingredients": [*recipes[key].get("ingredients", []), {
                    "order": ing["IRDNT_SN"],
                    "name_kr": ing["IRDNT_NM"], 
                    "amount": ing["IRDNT_CPCTY"], 
                    "type_code": ing["IRDNT_TY_NM"], 
                    "type_kr": ing["IRDNT_TY_CODE"],
                }]
            }
            
        new_recipes = list(recipes.values())

        neo_result = neo4j_db.execute_write(
            query="""
                UNWIND $recipes AS recipe
                MERGE (r:Recipe { recipe_id: recipe.recipe_id })
                ON CREATE
                    SET r.uuid = randomUUID(),
                        r.created_at = datetime()
                ON MATCH
                    SET r.updated_at = datetime()

                WITH r, recipe

                UNWIND recipe.ingredients AS ing
                MERGE (i:Ingredient { name: ing.name_kr })
                ON CREATE
                    SET i.uuid = randomUUID(),
                        i.created_at = datetime()
                ON MATCH 
                    SET i.updated_at = datetime()
                
                MERGE (r)-[m:MADE_BY]->(i)
                ON CREATE
                    SET m.order = ing.order,
                        m.amount = ing.amount,
                        m.type = ing.type_kr,
                        m.type_code = ing.type_code,
                        m.created_at = datetime()
                ON MATCH
                    SET m.updated_at = datetime()
            """,
            params={ "recipes": new_recipes }
        )
        
        return neo_result
