# pdf_processor.py (fragmento relevante)
import os
import re
import fitz  # PyMuPDF
from sqlalchemy import Column, String, Integer, Boolean
from sqlalchemy.orm import sessionmaker
from models import engine, Base  # Reutilizamos el engine y Base

Session = sessionmaker(bind=engine)

class PDFData(Base):
    __tablename__ = "pdf_data"
    id = Column(Integer, primary_key=True, autoincrement=True)
    fecha = Column(String, nullable=True)
    pdf_id = Column(String, nullable=True)
    ciudad = Column(String, nullable=True)
    obra_publica = Column(Boolean, default=False)
    titulos = Column(String, nullable=True)
    texto = Column(String, nullable=False)

Base.metadata.create_all(engine)

# Resto del código para extraer y guardar información en la base de datos...
