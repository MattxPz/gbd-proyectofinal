from dotenv import load_dotenv
import os
import json
from pymongo import MongoClient

load_dotenv()
client = MongoClient(os.environ["MONGODB_URI"])
coleccion = client["streaming_db"]["producciones"]

pipeline = [
    {"$match": {"fecha_estreno": {"$gte": "2024-01-01", "$lte": "2024-12-31"}}},
    {"$sort": {"fecha_estreno": 1}},
]

plan = coleccion.database.command(
    "explain",
    {"aggregate": "producciones", "pipeline": pipeline, "cursor": {}},
    verbosity="executionStats",
)

print(json.dumps(plan["queryPlanner"]["winningPlan"], indent=2))