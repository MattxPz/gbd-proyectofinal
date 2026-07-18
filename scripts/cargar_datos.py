"""Carga data/datos.json en la colección 'producciones' de streaming_db."""
import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, PyMongoError

BASE_DIR = Path(__file__).resolve().parent.parent
DATOS_PATH = BASE_DIR / "data" / "datos.json"

load_dotenv(BASE_DIR / ".env")


def main():
    mongodb_uri = os.getenv("MONGODB_URI")
    if not mongodb_uri:
        print("Error: la variable MONGODB_URI no está definida en .env")
        sys.exit(1)

    try:
        with open(DATOS_PATH, encoding="utf-8") as f:
            documentos = json.load(f)
    except FileNotFoundError:
        print(f"Error: no se encontró el archivo {DATOS_PATH}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: el archivo {DATOS_PATH} no contiene JSON válido: {e}")
        sys.exit(1)

    if not documentos:
        print(f"Error: {DATOS_PATH} no contiene documentos para cargar")
        sys.exit(1)

    try:
        client = MongoClient(mongodb_uri, serverSelectionTimeoutMS=5000)
        client.admin.command("ping")
    except ConnectionFailure as e:
        print(f"Error: no se pudo conectar a MongoDB: {e}")
        sys.exit(1)

    try:
        db = client["streaming_db"]
        coleccion = db["producciones"]

        if coleccion.count_documents({}) > 0:
            coleccion.delete_many({})
            print("Colección 'producciones' vaciada.")

        coleccion.insert_many(documentos)
    except PyMongoError as e:
        print(f"Error al cargar los datos en MongoDB: {e}")
        sys.exit(1)
    finally:
        total = client["streaming_db"]["producciones"].count_documents({})
        client.close()

    print(f"Carga completada. La colección 'producciones' tiene {total} documentos.")


if __name__ == "__main__":
    main()
