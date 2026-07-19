"""Páginas HTML (Jinja2) para mostrar los 5 reportes en una demo.

Reutiliza los mismos pipelines de app/aggregations.py que usan los
endpoints JSON en app/routes/reportes.py; solo cambia el formato de
salida (render_template en vez de jsonify).
"""
import unicodedata

from flask import Blueprint, render_template, request
from pymongo.errors import PyMongoError

from app import aggregations
from app.db import get_producciones_collection

vistas_bp = Blueprint("vistas", __name__)


@vistas_bp.route("/")
def index():
    # Estadísticas rápidas para el dashboard, calculadas en vivo contra
    # MongoDB Atlas. Si la conexión falla, se muestra el panel igual pero
    # sin datos y con el estado de conexión en "error" (ver base.html).
    stats = None
    db_conectado = True
    try:
        coleccion = get_producciones_collection()
        stats = {
            "total_producciones": coleccion.count_documents({}),
            "total_generos": len(coleccion.distinct("generos")),
            "total_actores": len(coleccion.distinct("actores_principales.actor_id")),
        }
    except PyMongoError:
        db_conectado = False

    return render_template("index.html", stats=stats, db_conectado=db_conectado)


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


def _sin_acentos(texto):
    """Quita acentos/diacríticos para que el orden alfabético no separe,
    por ejemplo, "Núñez" de "Nunez" en distintos bloques."""
    normalizado = unicodedata.normalize("NFKD", texto)
    return "".join(c for c in normalizado if not unicodedata.combining(c))


@vistas_bp.route("/vista/por-genero")
def vista_por_genero():
    genero = request.args.get("genero", "")

    resultados = []
    if genero:
        resultados = aggregations.producciones_por_genero(get_producciones_collection(), genero)

    # Géneros distintos en la colección, para ofrecerlos como sugerencias
    # de autocompletado en el campo de búsqueda (ver <datalist> en la plantilla).
    generos_disponibles = sorted(get_producciones_collection().distinct("generos"))

    return render_template(
        "reporte_genero.html",
        resultados=resultados,
        genero=genero,
        generos_disponibles=generos_disponibles,
    )


@vistas_bp.route("/vista/por-actor")
def vista_por_actor():
    actor = request.args.get("actor", "")

    resultados = []
    if actor:
        resultados = aggregations.producciones_por_actor(get_producciones_collection(), actor)

    # Listado completo de actores para mostrar en pantalla, ordenado
    # alfabéticamente por apellido (última palabra del nombre completo).
    actores = aggregations.todos_los_actores(get_producciones_collection())
    actores_disponibles = sorted(
        actores, key=lambda a: _sin_acentos(a["nombre"].split()[-1]).lower()
    )

    return render_template(
        "reporte_actor.html",
        resultados=resultados,
        actor=actor,
        actores_disponibles=actores_disponibles,
    )


@vistas_bp.route("/vista/actores-mas-participaciones")
def vista_actores_mas_participaciones():
    n = request.args.get("n", default=10, type=int)
    resultados = aggregations.actores_con_mas_participaciones(get_producciones_collection(), n)
    return render_template("reporte_actores.html", resultados=resultados, n=n)
