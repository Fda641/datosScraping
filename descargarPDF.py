# descargarPDF.py
import os
import sys
import requests
import re
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

# Función para verificar si las librerías necesarias están instaladas
def verificar_librerias():
    try:
        import requests
        import bs4
        print("Todas las librerías necesarias están instaladas.\n")
    except ImportError as e:
        print(f"Error: Falta una librería necesaria: {e.name}")
        print("Instale las librerías necesarias con el siguiente comando: ")
        print("pip install requests beautifulsoup4")
        sys.exit(1)  # Termina la ejecución del script

# Función para verificar si la carpeta "ContenedoraPDF" existe
# Si no existe, la crea y devuelve su ruta
def verificar_carpeta():
    carpeta = "ContenedoraPDF"
    ruta_carpeta = os.path.join(os.path.dirname(os.path.abspath(__file__)), carpeta)
    
    if not os.path.exists(ruta_carpeta):
        print(f"La carpeta '{carpeta}' no existe. Creándola...")
        os.makedirs(ruta_carpeta)  # Crea la carpeta
    else:
        print(f"La carpeta '{carpeta}' existe.")
    
    print(f"Ruta de la carpeta: {ruta_carpeta}\n")
    return ruta_carpeta

# Función para obtener la fecha y asegurarse de que no sea domingo
def obtener_fecha():
    while True:
        fecha_str = input("Ingrese la fecha en formato YYYY/MM/DD: ")
        try:
            fecha = datetime.strptime(fecha_str, "%Y/%m/%d")  # Valida el formato de fecha
            # Verifica si la fecha es un domingo
            if fecha.weekday() == 6:  # 6 corresponde a domingo
                print("La fecha ingresada es un domingo. Se ajustará al sábado anterior.")
                # Ajusta la fecha al sábado (restando 1 día)
                fecha -= timedelta(days=1)
                fecha_str = fecha.strftime("%Y/%m/%d")
            return fecha_str
        except ValueError:
            print("Formato incorrecto. Intente nuevamente.")

# Función para generar una URL basada en la fecha ingresada por el usuario
def modificar_url(fecha):
    url_base = "https://www.boe.es/boe/dias/"
    nueva_url = f"{url_base}{fecha}/"  # Construye la URL con la fecha
    print("Nueva URL:", nueva_url)
    return nueva_url

# Función para extraer todos los enlaces de la página y clasificarlos en PDFs y HTMLs
def extraer_links(url):
    try:
        respuesta = requests.get(url)  # Realiza la solicitud a la URL
        if respuesta.status_code == 200:
            soup = BeautifulSoup(respuesta.text, 'html.parser')  # Analiza el HTML de la página
            links = [a['href'] for a in soup.find_all('a', href=True)]  # Encuentra todos los enlaces
            
            pdf_links = []  # Lista para almacenar enlaces a archivos PDF
            html_links = []  # Lista para almacenar enlaces a archivos HTML
            
            for link in links:
                if link.endswith(".pdf"):
                    pdf_links.append(requests.compat.urljoin(url, link))  # Convierte enlaces relativos a absolutos
                elif link.endswith(".html"):
                    html_links.append(requests.compat.urljoin(url, link))
            
            print("\nLinks a archivos PDF:")
            for link in pdf_links:
                print(link)
            
            print("\nLinks a archivos HTML:")
            for link in html_links:
                print(link)
            
            if not pdf_links and not html_links:
                print("No se encontraron enlaces a archivos PDF o HTML.")
            
            return pdf_links  # Devuelve los enlaces a archivos PDF
        else:
            print("No se pudo acceder a la página.")
            return []
    except requests.exceptions.RequestException as e:
        print("Error al obtener la URL:", e)
        return []

# Función para descargar los archivos PDF y guardarlos en la carpeta especificada
def descargar_pdfs(pdf_links, carpeta):
    for link in pdf_links:
        nombre_archivo = os.path.join(carpeta, os.path.basename(link))  # Nombre del archivo descargado
        try:
            print(f"Descargando {link} ...")
            respuesta = requests.get(link, stream=True)  # Descarga el archivo en fragmentos
            if respuesta.status_code == 200:
                with open(nombre_archivo, 'wb') as archivo:
                    for chunk in respuesta.iter_content(chunk_size=1024):  # Escribe el archivo en bloques de 1024 bytes
                        archivo.write(chunk)
                print(f"Descargado: {nombre_archivo}")
            else:
                print(f"No se pudo descargar: {link}")
        except requests.exceptions.RequestException as e:
            print(f"Error al descargar {link}: {e}")

# Bloque principal del programa
if __name__ == "__main__":
    verificar_librerias()  # Verifica si las librerías necesarias están instaladas
    carpeta_pdf = verificar_carpeta()  # Verifica o crea la carpeta de almacenamiento
    fecha = obtener_fecha()  # Obtiene la fecha ingresada por el usuario
    url = modificar_url(fecha)  # Modifica la URL con la fecha ingresada
    pdf_links = extraer_links(url)  # Extrae los enlaces de la página
    if pdf_links:
        descargar_pdfs(pdf_links, carpeta_pdf)  # Descarga los archivos PDF si existen
