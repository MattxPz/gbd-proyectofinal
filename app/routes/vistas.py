"""Páginas HTML (Jinja2) para mostrar los 5 reportes en una demo.

Reutiliza los mismos pipelines de app/aggregations.py que usan los
endpoints JSON en app/routes/reportes.py; solo cambia el formato de
salida (render_template en vez de jsonify).
"""
from flask import Blueprint, render_template, request

from app import aggregations
from app.db import get_producciones_collection

vistas_bp = Blueprint("vistas", __name__)


@vistas_bp.route("/")
def index():
    return render_template("index.html")


@vistas_bp.route("/vista/periodo")
def vista_periodo():
    fecha_inicio = request.args.get("fecha_inicio", "")
    fecha_fin = request.args.get("fecha_fin", "")

    resultados = []
    if fecha_inicio and fecha_fin:
        resultados = aggregations.producciones_por_periodo(
            get_producciones_collection(), fecha_inicio, fecha_fin
        )

    return render_template(
        "reporte_periodo.html",
        resultados=resultados,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
    )


@vistas_bp.route("/vista/top-reproducciones")
def vista_top_reproducciones():
    n = request.args.get("n", default=10, type=int)
    resultados = aggregations.top_reproducciones(get_producciones_collection(), n)
    return render_template("reporte_top.html", resultados=resultados, n=n)


@vistas_bp.route("/vista/por-genero")
def vista_por_genero():
    genero = request.args.get("genero", "")

    resultados = []
    if genero:
        resultados = aggregations.producciones_por_genero(get_producciones_collection(), genero)

    return render_template("reporte_genero.html", resultados=resultados, genero=genero)


@vistas_bp.route("/vista/por-actor")
def vista_por_actor():
    actor = request.args.get("actor", "")

    resultados = []
    if actor:
        resultados = aggregations.producciones_por_actor(get_producciones_collection(), actor)

    return render_template("reporte_actor.html", resultados=resultados, actor=actor)


@vistas_bp.route("/vista/actores-mas-participaciones")
def vista_actores_mas_participaciones():
    n = request.args.get("n", default=10, type=int)
    resultados = aggregations.actores_con_mas_participaciones(get_producciones_collection(), n)
    return render_template("reporte_actores.html", resultados=resultados, n=n)
