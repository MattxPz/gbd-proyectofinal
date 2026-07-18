"""Conexión a MongoDB para la aplicación Flask."""
import os
from pathlib import Path

from dotenv import load_dotenv
from pymongo import MongoClient

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

_client = None


def get_client():
    """Devuelve un MongoClient reutilizable (una sola conexión por proceso)."""
    global _client
    if _client is None:
        uri = os.getenv("MONGODB_URI")
        if not uri:
            raise RuntimeError("La variable MONGODB_URI no está definida en .env")
        _client = MongoClient(uri, serverSelectionTimeoutMS=5000)
    return _client


def get_db():
    return get_client()["streaming_db"]


def get_producciones_collection():
    return get_db()["producciones"]
