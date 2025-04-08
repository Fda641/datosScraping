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

# ➕ Palabras clave de interés
PALABRAS_CLAVE = ["paredes ventiladas", "falsos techos", "fachadas ventiladas", "revestimiento acústico"]

# ➕ Patrón para ciudad (esto se puede ajustar)
CIUDAD_REGEX = re.compile(r"(Madrid|Barcelona|Valencia|Sevilla|Bilbao|Zaragoza|Málaga|.*?Ayuntamiento)", re.IGNORECASE)

# ➕ Función para procesar un PDF
def procesar_pdf(ruta_pdf, pdf_id=None, fecha=None):
    session = Session()
    doc = fitz.open(ruta_pdf)
    texto_total = ""
    titulos_detectados = []
    ciudad_detectada = None
    obra_publica = False

    for page in doc:
        texto = page.get_text()
        texto_total += texto + "\n"

        # Buscar palabras clave
        if any(palabra in texto.lower() for palabra in PALABRAS_CLAVE):
            obra_publica = True

        # Buscar ciudad
        if not ciudad_detectada:
            match = CIUDAD_REGEX.search(texto)
            if match:
                ciudad_detectada = match.group()

        # Detectar títulos potenciales (puedes mejorarlo con heurísticas)
        titulos = re.findall(r'(?i)(LICITACIÓN|CONTRATACIÓN|PROYECTO DE OBRAS.*?)\n', texto)
        titulos_detectados.extend(titulos)

    if obra_publica:
        entry = PDFData(
            fecha=fecha,
            pdf_id=pdf_id or os.path.basename(ruta_pdf),
            ciudad=ciudad_detectada,
            obra_publica=True,
            titulos=" | ".join(set(titulos_detectados)),
            texto=texto_total[:5000]  # Guarda solo un resumen si es muy largo
        )
        session.add(entry)
        session.commit()
        print(f"✅ Guardado: {ruta_pdf}")
    else:
        print(f"⏭️ No relevante: {ruta_pdf}")
    
    session.close()
