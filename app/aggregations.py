"""Pipelines de agregación de MongoDB para los reportes del catálogo.

Nota sobre 'fecha_estreno': se almacena como string en formato ISO
"YYYY-MM-DD". Ese formato conserva el orden cronológico al compararse
como texto (lexicográficamente), por lo que $gte/$lte y $sort funcionan
igual que con un tipo Date, sin necesidad de convertir el campo.
"""


def producciones_por_periodo(coleccion, fecha_inicio, fecha_fin):
    """Reporte 1: producciones estrenadas en un período [fecha_inicio, fecha_fin]."""
    pipeline = [
        # Etapa 1 ($match): conserva solo los documentos cuya fecha_estreno
        # cae dentro del rango solicitado (ambos límites inclusive).
        {"$match": {"fecha_estreno": {"$gte": fecha_inicio, "$lte": fecha_fin}}},
        # Etapa 2 ($sort): ordena el resultado cronológicamente para que el
        # reporte se lea como una línea de tiempo.
        {"$sort": {"fecha_estreno": 1}},
    ]
    return list(coleccion.aggregate(pipeline))


def top_reproducciones(coleccion, limite=10):
    """Reporte 2: producciones con mayor número de reproducciones (top N)."""
    # $limit exige un entero positivo: con n=0 o negativo Mongo rechaza el
    # pipeline entero (OperationFailure), así que se acota a un mínimo de 1.
    limite = max(1, limite)
    pipeline = [
        # Etapa 1 ($sort): ordena todas las producciones de mayor a menor
        # numero_reproducciones. Al usar el índice descendente sobre este
        # campo, Mongo puede resolver el sort directamente desde el índice.
        {"$sort": {"numero_reproducciones": -1}},
        # Etapa 2 ($limit): recorta el resultado a los N primeros (el "top N"
        # pedido por el reporte).
        {"$limit": limite},
    ]
    return list(coleccion.aggregate(pipeline))


def producciones_por_genero(coleccion, genero):
    """Reporte 3: producciones que pertenecen a un género determinado."""
    pipeline = [
        # Etapa 1 ($match): 'generos' es un array; al comparar el campo
        # contra un valor escalar, Mongo hace match si CUALQUIER elemento
        # del array es igual a ese valor (semántica implícita de array).
        {"$match": {"generos": genero}},
        # Etapa 2 ($sort): las más recientes primero, solo para presentación.
        {"$sort": {"fecha_estreno": -1}},
    ]
    return list(coleccion.aggregate(pipeline))


def producciones_por_actor(coleccion, nombre_actor):
    """Reporte 4: producciones donde participa un actor determinado."""
    pipeline = [
        # Etapa 1 ($match): 'actores_principales' es un array de subdocumentos;
        # esta forma de dot-notation filtra los documentos donde ALGÚN
        # elemento del array tiene ese valor en su campo 'nombre'.
        {"$match": {"actores_principales.nombre": nombre_actor}},
        {"$sort": {"fecha_estreno": -1}},
    ]
    return list(coleccion.aggregate(pipeline))


def actores_con_mas_participaciones(coleccion, limite=10):
    """Reporte 5: actores con mayor número de participaciones (agrupado)."""
    # Mismo límite mínimo de 1 que en top_reproducciones (ver comentario ahí).
    limite = max(1, limite)
    pipeline = [
        # Etapa 1 ($unwind): "desenrolla" el array actores_principales,
        # generando un documento independiente por cada actor de cada
        # producción. Es el paso que permite agrupar por actor en lugar
        # de por producción.
        {"$unwind": "$actores_principales"},
        # Etapa 2 ($group): agrupa esos documentos por actor_id (identificador
        # estable, evita duplicados por variaciones de escritura del nombre),
        # cuenta cuántas veces aparece ($sum: 1 = número de participaciones)
        # y conserva el nombre del actor para mostrarlo en el reporte.
        {
            "$group": {
                "_id": "$actores_principales.actor_id",
                "nombre": {"$first": "$actores_principales.nombre"},
                "participaciones": {"$sum": 1},
            }
        },
        # Etapa 3 ($sort): ordena de mayor a menor número de participaciones.
        {"$sort": {"participaciones": -1}},
        # Etapa 4 ($limit): recorta al top N solicitado.
        {"$limit": limite},
    ]
    return list(coleccion.aggregate(pipeline))


def todos_los_actores(coleccion):
    """Lista de todos los actores distintos del catálogo (sin límite ni orden
    de participaciones). Se usa para el listado de selección en el reporte
    por actor; el orden alfabético por apellido se aplica en Python porque
    el nombre completo se guarda como un único string."""
    pipeline = [
        # Mismo $unwind + $group por actor_id que en actores_con_mas_participaciones,
        # pero aquí solo interesa la lista de actores únicos, no su conteo.
        {"$unwind": "$actores_principales"},
        {
            "$group": {
                "_id": "$actores_principales.actor_id",
                "nombre": {"$first": "$actores_principales.nombre"},
            }
        },
    ]
    return list(coleccion.aggregate(pipeline))
