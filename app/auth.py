"""Validación de API key para proteger operaciones de escritura."""
import os

from flask import jsonify, request

METODOS_PROTEGIDOS = {"POST", "PUT", "DELETE"}


def validar_api_key():
    """Antes de un POST/PUT/DELETE, exige que el header X-API-KEY coincida
    con la variable de entorno API_KEY. Los GET no se validan."""
    if request.method not in METODOS_PROTEGIDOS:
        return None

    api_key_esperada = os.environ.get("API_KEY")
    api_key_recibida = request.headers.get("X-API-KEY")

    if not api_key_esperada or api_key_recibida != api_key_esperada:
        return jsonify({"error": "No autorizado"}), 401

    return None
