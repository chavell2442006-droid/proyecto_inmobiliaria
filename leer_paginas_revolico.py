from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd


carpeta = Path("paginas_revolico")

archivos = list(carpeta.glob("*.html"))
archivos += list(carpeta.glob("*.htm"))
archivos = sorted(set(archivos))

print("Páginas encontradas:", len(archivos))

anuncios = {}


for archivo in archivos:

    print("Leyendo:", archivo.name)

    with open(
        archivo,
        "r",
        encoding="utf-8",
        errors="ignore"
    ) as f:
        html = f.read()

    soup = BeautifulSoup(html, "html.parser")

    enlaces = soup.find_all("a", href=True)

    for enlace in enlaces:

        direccion = enlace.get("href", "")

        if (
            "/item/" not in direccion
            or "/item/publish" in direccion
        ):
            continue

        titulo = enlace.get_text(
            " ",
            strip=True
        )

        if not titulo:
            continue

        url = urljoin(
            "https://www.revolico.com",
            direccion
        )

        # Nivel 2: último contenedor que
        # pertenece solamente a ese anuncio
        contenedor = enlace

        for _ in range(2):
            if contenedor.parent is not None:
                contenedor = contenedor.parent

        texto_tarjeta = contenedor.get_text(
            " ",
            strip=True
        )

        anuncios[url] = {
            "titulo": titulo,
            "texto_tarjeta": texto_tarjeta,
            "url": url,
            "pagina_origen": archivo.name
        }


tabla = pd.DataFrame(
    anuncios.values()
)

print("\n--- RESULTADO ---")
print("Anuncios únicos:", len(tabla))

print("\nPrimeros anuncios:")
print(tabla.head(10))

tabla.to_csv(
    "enlaces_anuncios_revolico.csv",
    index=False,
    encoding="utf-8-sig"
)

print(
    "\nArchivo enlaces_anuncios_revolico.csv guardado."
)