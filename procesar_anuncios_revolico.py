import pandas as pd
import re


# Abrimos el archivo que creamos anteriormente
anuncios = pd.read_csv("enlaces_anuncios_revolico.csv")
def clasificar_anuncio(titulo):
    titulo = str(titulo).lower()

    palabras_excluir = [
        "busco alquiler",
        "busco casa",
        "busco apartamento",
        "compro casa",
        "compro apartamento",
        "se busca casa",
        "se busca apartamento",
        "alquiler",
        "se vende terreno",
        "vendo terreno"
    ]

    for palabra in palabras_excluir:
        if palabra in titulo:
            return "NO"

    return "SI"

anuncios["sirve_proyecto"] = anuncios["titulo"].apply(clasificar_anuncio)

print("\n--- CLASIFICACIÓN ---")

print(anuncios["sirve_proyecto"].value_counts())

print("\nEjemplos que NO sirven para el proyecto:")

print(
    anuncios[
        anuncios["sirve_proyecto"] == "NO"
    ][["titulo", "url"]].head(20)
)
# Quitamos enlaces que no son anuncios reales
anuncios = anuncios[
    ~anuncios["url"].str.contains("/item/publish", case=False, na=False)
].copy()

anuncios = anuncios[
    anuncios["titulo"].str.strip().str.lower() != "publicar"
].copy()
print("Cantidad de anuncios cargados:")
print(len(anuncios))

# Función para intentar sacar el precio del título
def extraer_precio(titulo):
    titulo = str(titulo)

    encontrado = re.match(r"\s*([\d.,]+)", titulo)

    if encontrado:
        precio_texto = encontrado.group(1)

        # Quitamos puntos y comas
        precio_limpio = re.sub(r"[^\d]", "", precio_texto)

        if precio_limpio:
            return int(precio_limpio)

    return None


# Función para detectar moneda
def extraer_moneda(titulo):
    titulo = str(titulo).upper()

    if "USD" in titulo:
        return "USD"

    if "CUP" in titulo:
        return "CUP"

    if "EUR" in titulo:
        return "EUR"

    if "MLC" in titulo:
        return "MLC"

    return None


anuncios["precio"] = anuncios["titulo"].apply(extraer_precio)

anuncios["moneda"] = anuncios["titulo"].apply(extraer_moneda)

print("\nPrimeros 10 anuncios procesados:")

print(
    anuncios[
        ["titulo", "precio", "moneda", "url"]
    ].head(10)
)

print("\nAnuncios donde encontramos precio:")
print(anuncios["precio"].notna().sum())

print("\nAnuncios donde NO encontramos precio:")
print(anuncios["precio"].isna().sum())

anuncios.to_csv(
    "anuncios_revolico_procesados.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nArchivo anuncios_revolico_procesados.csv guardado.")

print("\n--- EJEMPLOS SIN PRECIO ---")

sin_precio = anuncios[anuncios["precio"].isna()]

print(sin_precio[["titulo", "url"]].head(20))