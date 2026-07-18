"""Endpoints de reportes, cada uno respaldado por un pipeline de agregación
definido en app/aggregations.py (ver ese archivo para el detalle de cada etapa)."""
from flask import Blueprint, jsonify, request

from app import aggregations
from app.db import get_producciones_collection
from app.utils import serialize_doc

reportes_bp = Blueprint("reportes", __name__, url_prefix="/reportes")


@reportes_bp.route("/periodo", methods=["GET"])
def reporte_periodo():
    fecha_inicio = request.args.get("fecha_inicio")
    fecha_fin = request.args.get("fecha_fin")
    if not fecha_inicio or not fecha_fin:
        return jsonify({"error": "Se requieren 'fecha_inicio' y 'fecha_fin' (YYYY-MM-DD)"}), 400

    resultados = aggregations.producciones_por_periodo(
        get_producciones_collection(), fecha_inicio, fecha_fin
    )
    return jsonify([serialize_doc(doc) for doc in resultados]), 200


@reportes_bp.route("/top-reproducciones", methods=["GET"])
def reporte_top_reproducciones():
    limite = request.args.get("n", default=10, type=int)

    resultados = aggregations.top_reproducciones(get_producciones_collection(), limite)
    return jsonify([serialize_doc(doc) for doc in resultados]), 200


@reportes_bp.route("/por-genero", methods=["GET"])
def reporte_por_genero():
    genero = request.args.get("genero")
    if not genero:
        return jsonify({"error": "Se requiere el parámetro 'genero'"}), 400

    resultados = aggregations.producciones_por_genero(get_producciones_collection(), genero)
    return jsonify([serialize_doc(doc) for doc in resultados]), 200


@reportes_bp.route("/por-actor", methods=["GET"])
def reporte_por_actor():
    actor = request.args.get("actor")
    if not actor:
        return jsonify({"error": "Se requiere el parámetro 'actor' (nombre del actor)"}), 400

    resultados = aggregations.producciones_por_actor(get_producciones_collection(), actor)
    return jsonify([serialize_doc(doc) for doc in resultados]), 200


@reportes_bp.route("/actores-mas-participaciones", methods=["GET"])
def reporte_actores_mas_participaciones():
    limite = request.args.get("n", default=10, type=int)

    resultados = aggregations.actores_con_mas_participaciones(
        get_producciones_collection(), limite
    )
    # Aquí _id es el actor_id (entero), no un ObjectId: no requiere serialize_doc.
    return jsonify(resultados), 200
