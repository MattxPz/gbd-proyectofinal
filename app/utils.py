"""Utilidades compartidas por las rutas."""


def serialize_doc(doc):
    """Convierte un documento de MongoDB en un dict serializable a JSON.

    El único campo problemático para jsonify es '_id' (tipo ObjectId de BSON),
    por lo que se convierte a string. El resto de los campos del esquema
    (fechas como string ISO, arrays, subdocumentos) ya son JSON-nativos.
    """
    if doc is None:
        return None
    doc = dict(doc)
    doc["_id"] = str(doc["_id"])
    return doc
