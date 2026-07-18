"""Factory de la aplicación Flask del catálogo de streaming."""
from flask import Flask, jsonify


def create_app():
    app = Flask(__name__)

    from app.routes.producciones import producciones_bp
    from app.routes.reportes import reportes_bp
    from app.routes.vistas import vistas_bp

    app.register_blueprint(producciones_bp)
    app.register_blueprint(reportes_bp)
    app.register_blueprint(vistas_bp)

    @app.route("/status")
    def status():
        return jsonify({"servicio": "Catálogo de streaming", "estado": "activo"})

    return app
