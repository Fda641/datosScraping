# datosScraping

Para obtener datos del boe
# Licitaciones Construcción

Este proyecto extrae y visualiza datos de licitaciones de proyectos de construcción, edificaciones y reformas a partir de fuentes oficiales y servicios de mapas.

## 🚀 Tecnologías utilizadas

- **Python**: Lenguaje principal para extracción y procesamiento de datos.
- **SQLAlchemy**: ORM para gestionar la base de datos.
- **Flask**: Framework web para visualizar los datos.
- **DBeaver**: Cliente SQL para inspeccionar y gestionar la base de datos.
- **Fuentes de datos**:
  - [BOE (Boletín Oficial del Estado)](https://www.boe.es/)
  - [Google Maps](https://maps.google.com)

## 📌 Instalación y configuración 

1. Clonar el repositorio:
   
bash
   git clone https://github.com/Fda641/datosScraping
   cd datosScraping

2. Crear un entorno virtual e instalar dependencias:
   
bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   pip install -r requirements.txt

3. Configurar la base de datos en config.py.
4. Ejecutar la aplicación:
   
bash
   python app.py

5. Acceder a la web en http://localhost:5000

Quiero crear un README.md para un repositorio de GitHub
El objetivo conseguir los datos de las licitaciones pública de proyectos de construcción, edificaciones y reformas.
- Las fuentes son el BOE (Boletín Oficial del Estado Español) 
- Google Maps
 
Base de datos con Python SQLAlchemy
Pagina web con Python Flask para visualizar los datos de la base datos.
Utilizaremos dbeaver client para ver los datos mientras desarrollamos
—
https://github.com/langolierivi/Taller_SqlAlchemy
—
https://docs.google.com/document/d/137GeGcIM8MoX9__DRF3U9QSDOJQDmXjiiSuCt0MNz1c/edit?usp=drivesdk

mi
https://docs.google.com/document/d/17a0LzZnM2nISlifCMsZ-LRPsJ29YDVRxmdAovhCmxDg/edit?usp=sharing
https://github.com/Fda641/datosScraping/blob/main/README.md

## 📊 Base de datos

La base de datos almacena:
- Información de licitaciones (fecha, entidad convocante, presupuesto, etc.).
- Ubicaciones y detalles de los proyectos extraídos de Google Maps.

## 🔧 Desarrollo

Durante el desarrollo, utilizamos **DBeaver** para visualizar y manipular los datos de la base de datos SQLAlchemy.
https://dbeaver.io/

## 📝 Licencia

Este proyecto está bajo la licencia MIT. Ver el archivo LICENSE para más detalles.