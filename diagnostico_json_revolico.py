from pathlib import Path
from bs4 import BeautifulSoup
import json


carpeta = Path("paginas_revolico")

archivos = list(carpeta.glob("*.html"))
archivos += list(carpeta.glob("*.htm"))

archivos = sorted(set(archivos))

print("Archivos encontrados:", len(archivos))


def buscar_ids(objeto, encontrados):

    if isinstance(objeto, dict):

        if (
            "id" in objeto
            and "title" in objeto
            and "permalink" in objeto
        ):
            encontrados.add(str(objeto.get("id")))

        for valor in objeto.values():
            buscar_ids(valor, encontrados)

    elif isinstance(objeto, list):

        for elemento in objeto:
            buscar_ids(elemento, encontrados)


for archivo in archivos:

    with open(
        archivo,
        "r",
        encoding="utf-8",
        errors="ignore"
    ) as f:
        html = f.read()

    soup = BeautifulSoup(html, "html.parser")

    script = soup.find(
        "script",
        id="__NEXT_DATA__"
    )

    ids = set()

    if script and script.string:

        datos = json.loads(script.string)

        buscar_ids(datos, ids)

    print("\nArchivo:", archivo.name)
    print("Anuncios en JSON:", len(ids))

    if ids:
        print("Primeros IDs:", list(ids)[:5])