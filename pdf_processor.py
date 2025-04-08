import os
import re
import fitz  # PyMuPDF
from sqlalchemy import Column, String, Integer, Boolean
from sqlalchemy.orm import sessionmaker
from models import engine, Base

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

# Palabras clave
PALABRAS_CLAVE = ["paredes ventiladas", "falsos techos", "fachadas ventiladas", "techo registrable"]

def extraer_info_pdf(pdf_path):
    with fitz.open(pdf_path) as doc:
        texto_total = ""
        for page in doc:
            texto_total += page.get_text()

    # Filtrado básico por palabras clave
    texto_lower = texto_total.lower()
    relevante = any(palabra in texto_lower for palabra in PALABRAS_CLAVE)

    if not relevante:
        return None  # No guardar si no contiene temas relevantes

    # Extraer datos simples con regex
    ciudad = extraer_ciudad(texto_total)
    fecha = extraer_fecha(texto_total)
    titulos = extraer_titulos(texto_total)
    pdf_id = os.path.basename(pdf_path)

    return {
        "fecha": fecha,
        "pdf_id": pdf_id,
        "ciudad": ciudad,
        "obra_publica": True,
        "titulos": titulos,
        "texto": texto_total
    }

def extraer_ciudad(texto):
    match = re.search(r"(Provincia|Localidad):\s*(\w+)", texto, re.IGNORECASE)
    return match.group(2) if match else None

def extraer_fecha(texto):
    match = re.search(r"(\d{1,2}/\d{1,2}/\d{4})", texto)
    return match.group(1) if match else None

def extraer_titulos(texto):
    lineas = texto.splitlines()
    titulos = [linea.strip() for linea in lineas if linea.isupper() and len(linea.split()) > 2]
    return "; ".join(titulos[:3])  # Limita a 3 títulos

def procesar_pdfs(carpeta="ContenedoraPDF"):
    session = Session()
    for filename in os.listdir(carpeta):
        if filename.endswith(".pdf"):
            path = os.path.join(carpeta, filename)
            datos = extraer_info_pdf(path)
            if datos:
                entry = PDFData(**datos)
                session.add(entry)
                print(f"✅ Guardado: {filename}")
            else:
                print(f"⏭️ No relevante: {filename}")
    session.commit()
    session.close()

if __name__ == "__main__":
    procesar_pdfs()
