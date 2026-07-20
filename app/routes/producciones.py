"""CRUD de producciones (películas y series)."""
from bson import ObjectId
from bson.errors import InvalidId
from flask import Blueprint, jsonify, request

from app.auth import validar_api_key
from app.db import get_producciones_collection
from app.utils import serialize_doc

producciones_bp = Blueprint("producciones", __name__, url_prefix="/producciones")
producciones_bp.before_request(validar_api_key)


def _parse_object_id(id_produccion):
    try:
        return ObjectId(id_produccion), None
    except InvalidId:
        return None, (jsonify({"error": "Id inválido"}), 400)


@producciones_bp.route("", methods=["POST"])
def crear_produccion():
    datos = request.get_json(silent=True)
    if not datos:
        return jsonify({"error": "Se requiere un cuerpo JSON"}), 400
    if "tipo" not in datos or "nombre" not in datos:
        return jsonify({"error": "Los campos 'tipo' y 'nombre' son obligatorios"}), 400

    coleccion = get_producciones_collection()
    resultado = coleccion.insert_one(datos)
    creado = coleccion.find_one({"_id": resultado.inserted_id})
    return jsonify(serialize_doc(creado)), 201


@producciones_bp.route("", methods=["GET"])
def listar_producciones():
    coleccion = get_producciones_collection()

    tipo = request.args.get("tipo")
    filtro = {"tipo": tipo} if tipo else {}

    producciones = [serialize_doc(doc) for doc in coleccion.find(filtro)]
    return jsonify(producciones), 200


@producciones_bp.route("/<id_produccion>", methods=["GET"])
def obtener_produccion(id_produccion):
    oid, error = _parse_object_id(id_produccion)
    if error:
        return error

    doc = get_producciones_collection().find_one({"_id": oid})
    if not doc:
        return jsonify({"error": "Producción no encontrada"}), 404
    return jsonify(serialize_doc(doc)), 200


@producciones_bp.route("/<id_produccion>", methods=["PUT"])
def editar_produccion(id_produccion):
    oid, error = _parse_object_id(id_produccion)
    if error:
        return error

    datos = request.get_json(silent=True)
    if not datos:
        return jsonify({"error": "Se requiere un cuerpo JSON"}), 400
    datos.pop("_id", None)

    coleccion = get_producciones_collection()
    resultado = coleccion.update_one({"_id": oid}, {"$set": datos})
    if resultado.matched_count == 0:
        return jsonify({"error": "Producción no encontrada"}), 404

    actualizado = coleccion.find_one({"_id": oid})
    return jsonify(serialize_doc(actualizado)), 200


@producciones_bp.route("/<id_produccion>", methods=["DELETE"])
def eliminar_produccion(id_produccion):
    oid, error = _parse_object_id(id_produccion)
    if error:
        return error

    resultado = get_producciones_collection().delete_one({"_id": oid})
    if resultado.deleted_count == 0:
        return jsonify({"error": "Producción no encontrada"}), 404

    return jsonify({"mensaje": "Producción eliminada"}), 200
