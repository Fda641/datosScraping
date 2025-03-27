# app.py
from flask import Flask, render_template_string
from models import Session, Licitacion

app = Flask(__name__)

html_code = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Datos de Licitaciones</title>
    <style>
        /* Estilos para la página */
        body { font-family: Arial, sans-serif; background-color: #f4f4f9; padding: 20px; }
        .container { width: 80%; max-width: 800px; margin: 0 auto; text-align: center; }
        .data-list ul { list-style-type: none; padding: 0; }
        .data-list li { background-color: #f9f9f9; padding: 10px; margin: 10px 0; border-radius: 5px; border: 1px solid #ddd; }
    </style>
</head>
<body>
    <div class="container">
        <h2>Licitaciones</h2>
        <div class="data-list">
            <ul>
                {% for item in datos %}
                    <li>{{ item.fecha }} - {{ item.entidad }} - {{ item.presupuesto }}</li>
                {% endfor %}
            </ul>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    # Abrir una sesión SQLAlchemy
    session = Session()
    # Consultar todas las licitaciones
    licitaciones = session.query(Licitacion).all()
    # Preparar los datos para la plantilla
    datos = [
        {
            "fecha": lic.fecha,
            "entidad": lic.entidad,
            "presupuesto": lic.presupuesto
        }
        for lic in licitaciones
    ]
    session.close()
    return render_template_string(html_code, datos=datos)

if __name__ == '__main__':
    app.run(debug=True)
