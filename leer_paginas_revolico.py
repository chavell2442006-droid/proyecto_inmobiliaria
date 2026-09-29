from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd

carpeta = Path("paginas_revolico")

archivos = sorted(carpeta.glob("*.html"))

print("Cantidad de páginas encontradas:", len(archivos))

anuncios = {}

for archivo in archivos:
    print("\nLeyendo:", archivo.name)

    with open(archivo, "r", encoding="utf-8", errors="ignore") as f:
        html = f.read()

    soup = BeautifulSoup(html, "html.parser")

    enlaces = soup.find_all("a", href=True)

    for enlace in enlaces:
        direccion = enlace.get("href")
        titulo = enlace.get_text(" ", strip=True)

        if "/item/" in direccion and direccion != "/item/publicar" and titulo:
            url_completa = urljoin(
                "https://www.revolico.com",
                direccion
            )

            anuncios[url_completa] = titulo

print("\n--- RESULTADO ---")
print("Anuncios únicos encontrados:", len(anuncios))

datos = []

for url, titulo in anuncios.items():
    datos.append({
        "titulo": titulo,
        "url": url
    })

tabla = pd.DataFrame(datos)

print("\nPrimeros anuncios:")
print(tabla.head(10))

tabla.to_csv(
    "enlaces_anuncios_revolico.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nArchivo enlaces_anuncios_revolico.csv guardado correctamente.")