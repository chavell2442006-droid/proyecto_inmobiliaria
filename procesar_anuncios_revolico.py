import pandas as pd
import re


# -----------------------------------
# 1. CARGAR LOS ANUNCIOS
# -----------------------------------

anuncios = pd.read_csv("enlaces_anuncios_revolico.csv")

print("\n--- INICIO ---")
print("Anuncios cargados:", len(anuncios))


# -----------------------------------
# 2. LIMPIEZA INICIAL
# -----------------------------------

# Quitamos filas sin título o sin URL
anuncios = anuncios.dropna(subset=["titulo", "url"]).copy()

# Quitamos espacios sobrantes
anuncios["titulo"] = anuncios["titulo"].str.strip()
anuncios["url"] = anuncios["url"].str.strip()

# Quitamos el enlace de "Publicar"
anuncios = anuncios[
    ~anuncios["url"].str.contains(
        "/item/publish",
        case=False,
        na=False
    )
].copy()

# Quitamos también cualquier título que sea solamente "Publicar"
anuncios = anuncios[
    anuncios["titulo"].str.lower() != "publicar"
].copy()

# Por seguridad, quitamos URLs repetidas
anuncios = anuncios.drop_duplicates(subset=["url"]).copy()

print("Anuncios después de limpieza inicial:", len(anuncios))


# -----------------------------------
# 3. EXTRAER PRECIO
# -----------------------------------

def extraer_precio(titulo):

    titulo = str(titulo)

    # Busca un número al comienzo del título
    encontrado = re.match(
        r"\s*([\d.,]+)",
        titulo
    )

    if encontrado:

        precio_texto = encontrado.group(1)

        # Dejamos solamente los números
        precio_limpio = re.sub(
            r"[^\d]",
            "",
            precio_texto
        )

        if precio_limpio:
            return int(precio_limpio)

    return None


anuncios["precio"] = anuncios["titulo"].apply(extraer_precio)


# -----------------------------------
# 4. EXTRAER MONEDA
# -----------------------------------

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


anuncios["moneda"] = anuncios["titulo"].apply(extraer_moneda)


# -----------------------------------
# 5. CLASIFICAR ANUNCIOS
# -----------------------------------

def clasificar_anuncio(titulo):

    titulo = str(titulo).lower()

    # Estos claramente NO nos sirven
    palabras_excluir = [
        "busco alquiler",
        "busco casa",
        "busco apartamento",
        "busco apto",
        "compro casa",
        "compro apartamento",
        "compro apto",
        "se busca casa",
        "se busca apartamento",
        "se busca apto",
        "alquilo",
        "se alquila",
        "se vende terreno",
        "vendo terreno"
    ]

    for palabra in palabras_excluir:
        if palabra in titulo:
            return "NO"

    # Estos pueden ser dudosos y preferimos revisarlos
    palabras_revisar = [
        "cambio",
        "permuta",
        "detalles en la imagen"
    ]

    for palabra in palabras_revisar:
        if palabra in titulo:
            return "REVISAR"

    return "SI"


anuncios["sirve_proyecto"] = anuncios["titulo"].apply(
    clasificar_anuncio
)


# -----------------------------------
# 6. MOSTRAR RESUMEN
# -----------------------------------

print("\n--- PRECIOS ---")

print(
    "Anuncios donde encontramos precio:",
    anuncios["precio"].notna().sum()
)

print(
    "Anuncios donde NO encontramos precio:",
    anuncios["precio"].isna().sum()
)


print("\n--- CLASIFICACIÓN ---")

print(
    anuncios["sirve_proyecto"].value_counts()
)


# -----------------------------------
# 7. MOSTRAR EJEMPLOS SIN PRECIO
# -----------------------------------

sin_precio = anuncios[
    anuncios["precio"].isna()
]

print("\n--- EJEMPLOS SIN PRECIO ---")

print(
    sin_precio[
        ["titulo", "url"]
    ].head(20)
)


# -----------------------------------
# 8. SEPARAR LOS ANUNCIOS
# -----------------------------------

viviendas_candidatas = anuncios[
    anuncios["sirve_proyecto"] == "SI"
].copy()

revisar = anuncios[
    anuncios["sirve_proyecto"] == "REVISAR"
].copy()
excluidos = anuncios[
    anuncios["sirve_proyecto"] == "NO"
].copy()


# -----------------------------------
# 9. GUARDAR RESULTADOS
# -----------------------------------

anuncios.to_csv(
    "anuncios_revolico_procesados.csv",
    index=False,
    encoding="utf-8-sig"
)

viviendas_candidatas.to_csv(
    "viviendas_revolico_candidatas.csv",
    index=False,
    encoding="utf-8-sig"
)

revisar.to_csv(
    "anuncios_revolico_revisar.csv",
    index=False,
    encoding="utf-8-sig"
)

excluidos.to_csv(
    "anuncios_revolico_excluidos.csv",
    index=False,
    encoding="utf-8-sig"
)


print("\n--- ARCHIVOS GUARDADOS ---")

print("anuncios_revolico_procesados.csv")
print("viviendas_revolico_candidatas.csv")
print("anuncios_revolico_revisar.csv")
print("anuncios_revolico_excluidos.csv")

print("\nProceso terminado correctamente.")