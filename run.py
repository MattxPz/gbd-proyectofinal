from app import create_app

app = create_app()

if __name__ == "__main__":
    # use_reloader=False evita el hilo vigilante de auto-recarga de Werkzeug,
    # que en Windows provoca un traceback OSError [WinError 10038] al cerrar
    # el servidor con CTRL+C (bug conocido de Werkzeug, no del código de la
    # app). El auto-reload no es necesario para la demo: si editas el
    # código, basta con reiniciar manualmente.
    app.run(debug=True, use_reloader=False)
