# models.py
import os
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Configuración de la ruta de la base de datos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FOLDER = os.path.join(BASE_DIR, "BaseDatos_Scraping")
os.makedirs(DB_FOLDER, exist_ok=True)
DB_NAME = "licitaciones.db"
DB_PATH = os.path.join(DB_FOLDER, DB_NAME)

# Configuración del motor y la sesión con SQLAlchemy
engine = create_engine(f"sqlite:///{DB_PATH}", echo=False)
Session = sessionmaker(bind=engine)
Base = declarative_base()

# Definición del modelo para las licitaciones (ajusta campos según tu esquema)
class Licitacion(Base):
    __tablename__ = "licitaciones"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    fecha = Column(String, nullable=True)
    entidad = Column(String, nullable=True)
    presupuesto = Column(Float, nullable=True)
    descripcion = Column(String, nullable=True)
    # Agrega otros campos necesarios

# Crear las tablas en la base de datos si no existen
Base.metadata.create_all(engine)
