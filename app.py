from flask import Flask, render_template_string, request
from models import Session, Licitacion

app = Flask(__name__)

html_code = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Licitaciones Extraídas</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f4f4f9; padding: 20px; }
        .container { width: 80%; max-width: 900px; margin: 0 auto; }
        h1 { text-align: center; color: #333; }
        form { text-align: center; margin-bottom: 20px; }
        input[type="text"] { padding: 8px; width: 60%; border: 1px solid #ccc; border-radius: 4px; }
        button { padding: 8px 16px; border: none; background-color: #007BFF; color: white; border-radius: 4px; cursor: pointer; }
        .card { background-color: #fff; border-radius: 8px; padding: 15px; margin: 10px 0; border: 1px solid #ddd; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .card h3 { margin: 0 0 5px; color: #007BFF; }
        .card p { margin: 2px 0; color: #555; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Listado de Licitaciones</h1>
        <form method="GET">
            <input type="text" name="q" placeholder="Buscar por entidad o descripción..." value="{{ request.args.get('q', '') }}">
            <button type="submit">Buscar</button>
        </form>
        
        {% if datos %}
            {% for item in datos %}
                <div class="card">
                    <h3>{{ item.entidad }}</h3>
                    <p><strong>Fecha:</strong> {{ item.fecha }}</p>
                    <p><strong>Presupuesto:</strong> {{ item.presupuesto }} €</p>
                    <p><strong>Descripción:</strong> {{ item.descripcion }}</p>
                </div>
            {% endfor %}
        {% else %}
            <p>No hay resultados.</p>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    session = Session()
    try:
        busqueda = request.args.get('q', '')

        # Consulta condicional
        if busqueda:
            licitaciones = session.query(Licitacion).filter(
                (Licitacion.entidad.ilike(f"%{busqueda}%")) |
                (Licitacion.descripcion.ilike(f"%{busqueda}%"))
            ).all()
        else:
            licitaciones = session.query(Licitacion).all()

        datos = [
            {
                "fecha": lic.fecha,
                "entidad": lic.entidad,
                "presupuesto": lic.presupuesto,
                "descripcion": lic.descripcion
            }
            for lic in licitaciones
        ]
    finally:
        session.close()

    return render_template_string(html_code, datos=datos)

if __name__ == '__main__':
    app.run(debug=True)
