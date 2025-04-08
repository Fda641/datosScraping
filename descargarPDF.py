# descargarPDF.py

import os
import sys
import requests
import re
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

def verificar_librerias():
    try:
        import requests
        import bs4
        print("Todas las librerías necesarias están instaladas.\n")
    except ImportError as e:
        print(f"Error: Falta una librería necesaria: {e.name}")
        print("Instale las librerías necesarias con el siguiente comando: ")
        print("pip install requests beautifulsoup4")
        sys.exit(1)

def verificar_carpeta():
    carpeta = "ContenedoraPDF"
    ruta_carpeta = os.path.join(os.path.dirname(os.path.abspath(__file__)), carpeta)
    if not os.path.exists(ruta_carpeta):
        print(f"La carpeta '{carpeta}' no existe. Creándola...")
        os.makedirs(ruta_carpeta)
    else:
        print(f"La carpeta '{carpeta}' existe.")
    print(f"Ruta de la carpeta: {ruta_carpeta}\n")
    return ruta_carpeta

# Modificado: Obtener fecha automáticamente
def obtener_fecha():
    fecha = datetime.now()
    if fecha.weekday() == 6:  # Si es domingo
        print("Hoy es domingo. Se usará la fecha del sábado anterior.")
        fecha -= timedelta(days=1)
    fecha_str = fecha.strftime("%Y/%m/%d")
    print(f"Fecha utilizada: {fecha_str}")
    return fecha_str

def modificar_url(fecha):
    url_base = "https://www.boe.es/boe/dias/"
    nueva_url = f"{url_base}{fecha}/"
    print("Nueva URL:", nueva_url)
    return nueva_url

def extraer_links(url):
    try:
        respuesta = requests.get(url)
        if respuesta.status_code == 200:
            soup = BeautifulSoup(respuesta.text, 'html.parser')
            links = [a['href'] for a in soup.find_all('a', href=True)]
            pdf_links = [link for link in links if link.endswith('.pdf')]
            html_links = [link for link in links if not link.endswith('.pdf')]
            return pdf_links, html_links
        else:
            print("Error al acceder a la página:", url)
            return [], []
    except Exception as e:
        print("Error:", e)
        return [], []

if __name__ == "__main__":
    verificar_librerias()
    ruta_carpeta = verificar_carpeta()
    fecha = obtener_fecha()
    url = modificar_url(fecha)
    pdf_links, html_links = extraer_links(url)
    
    print(f"PDF encontrados: {len(pdf_links)}")
    print(f"HTML encontrados: {len(html_links)}")
