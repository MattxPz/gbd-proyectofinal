# Catálogo de Streaming — Gestión de Base de Datos

Proyecto final de la asignatura **Gestión de Base de Datos** (5to Ciclo). Aplicación web desarrollada con **Flask** y **MongoDB Atlas** que implementa un catálogo de producciones (películas y series) con operaciones CRUD completas y reportes basados en pipelines de agregación de MongoDB.

## Autores

- Mateo Paez
- Carlos Gordillo

## Diagrama del proyecto

![Diagrama Proyecto](docs/diagrama.png)

## Descripción

La aplicación permite administrar un catálogo de producciones audiovisuales almacenadas en MongoDB, cada una con géneros, actores principales, premios y estadísticas de reproducción. Sobre esa colección se exponen:

- Un **CRUD** completo vía API REST (`/producciones`).
- **5 reportes** basados en agregaciones de MongoDB, disponibles tanto como endpoints JSON (`/reportes/...`) como vistas HTML navegables (`/vista/...`).

## Tecnologías

- **Python 3.13**
- **Flask** — framework web y enrutamiento por blueprints
- **MongoDB Atlas** + **PyMongo** — persistencia y pipelines de agregación
- **Jinja2** — plantillas HTML para las vistas de reportes
- **python-dotenv** — manejo de variables de entorno
- **Gunicorn** — servidor WSGI para producción (Render)

## Estructura del proyecto

```
project-app/
├── app/
│   ├── __init__.py          # Factory de la app Flask (create_app)
│   ├── db.py                 # Conexión a MongoDB (cliente reutilizable)
│   ├── aggregations.py       # Pipelines de agregación de los 5 reportes
│   ├── utils.py               # Utilidades (serialización de documentos)
│   ├── routes/
│   │   ├── producciones.py   # CRUD de producciones (API REST)
│   │   ├── reportes.py       # Endpoints JSON de reportes
│   │   └── vistas.py          # Vistas HTML (dashboard y reportes)
│   ├── templates/            # Plantillas Jinja2 (dashboard + reportes)
│   └── static/css/           # Estilos de la aplicación
├── scripts/
│   ├── cargar_datos.py       # Carga data/datos.json en MongoDB
│   └── crear_indices.py      # Crea los índices de la colección
├── data/
│   └── datos.json            # Dataset de ejemplo (producciones)
├── run.py                    # Punto de entrada de la aplicación
├── requirements.txt
├── runtime.txt                # Versión de Python (Render)
├── .env.example               # Plantilla de variables de entorno
└── README.md
```

## Modelo de datos

Colección `producciones` en la base de datos `streaming_db`:

```json
{
  "tipo": "pelicula",
  "nombre": "El Origen del Código",
  "generos": ["Ciencia Ficción", "Suspenso"],
  "fecha_estreno": "2023-11-15",
  "duracion": 148,
  "numero_reproducciones": 1250000,
  "premios": [
    { "nombre": "Óscar", "categoria": "Mejores Efectos Visuales", "anio": 2024 }
  ],
  "actores_principales": [
    { "actor_id": 101, "nombre": "Ana Torres", "personaje": "Dra. Vega" }
  ]
}
```

Índices creados sobre la colección: `generos`, `actores_principales.actor_id`, `fecha_estreno` y `numero_reproducciones` (descendente).

## Instalación y configuración

### 1. Clonar el repositorio y crear el entorno virtual

```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Linux / macOS

pip install -r requirements.txt
```

### 2. Configurar variables de entorno

Copiar `.env.example` a `.env` y completar la cadena de conexión a MongoDB Atlas:

```
MONGODB_URI=mongodb+srv://usuario:password@cluster/...
PORT=5000
```

### 3. Cargar los datos de ejemplo

```bash
python scripts/cargar_datos.py
```

### 4. Crear los índices

```bash
python scripts/crear_indices.py
```

### 5. Ejecutar la aplicación

```bash
python run.py
```

La aplicación quedará disponible en `http://localhost:5000`.

## API REST — CRUD de producciones

| Método | Endpoint                     | Descripción                       |
|--------|-------------------------------|------------------------------------|
| POST   | `/producciones`               | Crea una nueva producción         |
| GET    | `/producciones`                | Lista producciones (filtro opcional `?tipo=`) |
| GET    | `/producciones/<id>`           | Obtiene una producción por id     |
| PUT    | `/producciones/<id>`           | Actualiza una producción          |
| DELETE | `/producciones/<id>`           | Elimina una producción            |

## Reportes (agregaciones)

Cada reporte tiene su endpoint JSON y su vista HTML equivalente:

| Reporte                            | Endpoint JSON                              | Vista HTML                       |
|-------------------------------------|---------------------------------------------|------------------------------------|
| Producciones por período de fechas | `GET /reportes/periodo?fecha_inicio=&fecha_fin=` | `/vista/periodo`            |
| Top de producciones más vistas     | `GET /reportes/top-reproducciones?n=`        | `/vista/top-reproducciones`      |
| Producciones por género             | `GET /reportes/por-genero?genero=`           | `/vista/por-genero`               |
| Producciones por actor              | `GET /reportes/por-actor?actor=`             | `/vista/por-actor`                |
| Actores con más participaciones     | `GET /reportes/actores-mas-participaciones?n=` | `/vista/actores-mas-participaciones` |

## Despliegue

El proyecto está configurado para desplegarse en **Render** (`runtime.txt`, `gunicorn` como servidor WSGI y lectura de `PORT` en tiempo de ejecución).

https://gbd-proyectofinal.onrender.com