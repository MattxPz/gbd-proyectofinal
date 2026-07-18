"""Crea los índices de la colección 'producciones' en streaming_db."""
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from pymongo import ASCENDING, DESCENDING, MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure, PyMongoError

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")

INDICES = [
    {"keys": [("generos", ASCENDING)], "name": "idx_generos"},
    {"keys": [("actores_principales.actor_id", ASCENDING)], "name": "idx_actores_principales"},
    {"keys": [("fecha_estreno", ASCENDING)], "name": "idx_fecha_estreno"},
    {"keys": [("numero_reproducciones", DESCENDING)], "name": "idx_numero_reproducciones"},
]


def main():
    mongodb_uri = os.getenv("MONGODB_URI")
    if not mongodb_uri:
        print("Error: la variable MONGODB_URI no está definida en .env")
        sys.exit(1)

    try:
        client = MongoClient(mongodb_uri, serverSelectionTimeoutMS=5000)
        client.admin.command("ping")
    except ConnectionFailure as e:
        print(f"Error: no se pudo conectar a MongoDB: {e}")
        sys.exit(1)

    coleccion = client["streaming_db"]["producciones"]

    for indice in INDICES:
        try:
            nombre = coleccion.create_index(indice["keys"], name=indice["name"])
            print(f"Índice creado o ya existente: {nombre}")
        except OperationFailure as e:
            print(f"Error al crear el índice {indice['name']}: {e}")
            sys.exit(1)
        except PyMongoError as e:
            print(f"Error inesperado al crear el índice {indice['name']}: {e}")
            sys.exit(1)

    print("\nÍndices actuales en 'producciones':")
    for info in coleccion.list_indexes():
        print(f"  - {info['name']}: {dict(info['key'])}")

    client.close()


if __name__ == "__main__":
    main()
