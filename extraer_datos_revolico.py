from pathlib import Path

from bs4 import BeautifulSoup

import json

import pandas as pd

carpeta = Path("paginas_revolico")

archivos = sorted(carpeta.glob("*.html"))

print("Páginas encontradas:", len(archivos))

anuncios = {}

def buscar_anuncios(objeto, archivo_origen):

    """

    Recorre el JSON buscando objetos que parezcan anuncios de Revolico.

    """

    if isinstance(objeto, dict):

        # Si tiene estos campos, probablemente es un anuncio

        if (

            "title" in objeto

            and "permalink" in objeto

            and "price" in objeto

        ):

            permalink = objeto.get("permalink")

            if permalink and "/item/" in str(permalink):

                url = "https://www.revolico.com" + permalink

                anuncios[url] = {

                    "id": objeto.get("id"),

                    "titulo": objeto.get("title"),

                    "precio": objeto.get("price"),

                    "moneda": objeto.get("currency"),

                    "municipio_id": objeto.get("municipalityId"),

                    "provincia_id": objeto.get("provinceId"),

                    "fecha_publicacion": objeto.get("publishedOnOrder"),

                    "promocionado": objeto.get("isPromoted"),

                    "cantidad_imagenes": objeto.get("imagesCount"),

                    "url": url,

                    "archivo_origen": archivo_origen

                }

        # Seguimos buscando dentro del diccionario

        for valor in objeto.values():

            buscar_anuncios(valor, archivo_origen)

    elif isinstance(objeto, list):

        for elemento in objeto:

            buscar_anuncios(elemento, archivo_origen)

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

    script = soup.find(

        "script",

        id="__NEXT_DATA__"

    )

    if script is None:

        print("No encontré NEXT_DATA en", archivo.name)

        continue

    try:

        datos = json.loads(script.string)

        buscar_anuncios(

            datos,

            archivo.name

        )

    except Exception as error:

        print(

            "Error procesando",

            archivo.name,

            ":",

            error)

print("\n--- RESULTADO ---")

print(

    "Anuncios estructurados únicos encontrados:",

    len(anuncios)

)

tabla = pd.DataFrame(

    anuncios.values()

)

print("\nPrimeros 10:")

print(tabla.head(10))

print("\nColumnas encontradas:")

print(tabla.columns.tolist())

tabla.to_csv(

    "datos_revolico_json.csv",

    index=False,

    encoding="utf-8-sig"

)

print(

    "\nArchivo datos_revolico_json.csv guardado correctamente.")